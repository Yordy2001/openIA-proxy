from typing import Dict, Optional, List
import uuid
from datetime import datetime, timedelta
from chat_models import AnalysisSession, ChatMessage
import json


class SessionService:
    """Service to manage analysis sessions and chat context"""
    
    def __init__(self):
        self.sessions: Dict[str, AnalysisSession] = {}
        self.session_timeout = timedelta(hours=24)  # Sessions expire after 24 hours
    
    def create_session(self, analysis_result: Dict, excel_data: Dict, file_names: List[str]) -> str:
        """Create a new analysis session"""
        session_id = str(uuid.uuid4())
        
        session = AnalysisSession(
            session_id=session_id,
            analysis_result=analysis_result,
            excel_data=excel_data,
            conversation_history=[],
            file_names=file_names
        )
        
        self.sessions[session_id] = session
        self.cleanup_expired_sessions()
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[AnalysisSession]:
        """Get a session by ID"""
        session = self.sessions.get(session_id)
        if session:
            # Update last activity
            session.last_activity = datetime.now()
            return session
        return None
    
    def add_message(self, session_id: str, message: ChatMessage) -> bool:
        """Add a message to the session conversation"""
        session = self.get_session(session_id)
        if session:
            session.conversation_history.append(message)
            session.last_activity = datetime.now()
            return True
        return False
    
    def get_conversation_context(self, session_id: str) -> str:
        """Get the full conversation context for AI processing"""
        session = self.get_session(session_id)
        if not session:
            return ""
        
        # Build context with Excel data, analysis results and conversation history
        context = f"""
ARCHIVOS ANALIZADOS: {', '.join(session.file_names)}
FECHA DEL ANÁLISIS: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}

DATOS ORIGINALES DEL EXCEL:
{session.excel_data.get('data', 'No disponible')}

RESUMEN DEL ANÁLISIS REALIZADO:
{session.analysis_result.get('summary', 'No disponible')}

HALLAZGOS ENCONTRADOS:
"""
        
        # Add findings with more detail
        findings = session.analysis_result.get('findings', [])
        for finding in findings:
            context += f"- [{finding.get('type', 'info').upper()}] {finding.get('title', 'Sin título')}\n"
            context += f"  Ubicación: {finding.get('location', 'No especificada')}\n"
            context += f"  Descripción: {finding.get('description', 'Sin descripción')}\n"
            context += f"  Severidad: {finding.get('severity', 'medium')}\n"
            context += f"  Solución sugerida: {finding.get('suggested_fix', 'No especificada')}\n\n"
        
        context += "RECOMENDACIONES:\n"
        recommendations = session.analysis_result.get('recommendations', [])
        for rec in recommendations:
            context += f"- {rec.get('title', 'Sin título')} (Prioridad: {rec.get('priority', 'medium')})\n"
            context += f"  {rec.get('description', 'Sin descripción')}\n\n"
        
        # Add metadata
        metadata = session.analysis_result.get('metadata', {})
        if metadata:
            context += f"INFORMACIÓN ADICIONAL:\n"
            context += f"- Total de hallazgos: {metadata.get('total_findings', 0)}\n"
            context += f"- Problemas críticos: {metadata.get('critical_issues', 0)}\n"
            context += f"- Hojas analizadas: {metadata.get('sheets_analyzed', 0)}\n"
            if metadata.get('non_profitable_bancas'):
                context += f"- Bancas no rentables: {', '.join(metadata.get('non_profitable_bancas', []))}\n"
            if metadata.get('possible_config_errors'):
                context += f"- Posibles errores de configuración: {', '.join(metadata.get('possible_config_errors', []))}\n"
        
        # Add recent conversation history
        context += "\nHISTORIAL DE CONVERSACIÓN RECIENTE:\n"
        for msg in session.conversation_history[-5:]:  # Last 5 messages
            role = "Usuario" if msg.role == "user" else "Asistente"
            context += f"{role}: {msg.content}\n"
        
        return context
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if current_time - session.last_activity > self.session_timeout
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
    
    def list_sessions(self) -> List[Dict]:
        """List all active sessions"""
        self.cleanup_expired_sessions()
        return [
            {
                "session_id": session.session_id,
                "file_names": session.file_names,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "message_count": len(session.conversation_history)
            }
            for session in self.sessions.values()
        ]
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


# Global session service instance
session_service = SessionService()
