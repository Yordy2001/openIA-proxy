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
        
        # Build context with analysis results and conversation history
        context = f"""
ANÁLISIS PREVIO:
Archivos analizados: {', '.join(session.file_names)}
Fecha del análisis: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}

RESUMEN DEL ANÁLISIS:
{session.analysis_result.get('summary', 'No disponible')}

HALLAZGOS:
"""
        
        # Add findings
        findings = session.analysis_result.get('findings', [])
        for i, finding in enumerate(findings[:5]):  # Limit to first 5 findings
            context += f"- {finding.get('title', 'Sin título')}: {finding.get('description', '')}\n"
        
        if len(findings) > 5:
            context += f"... y {len(findings) - 5} hallazgos más.\n"
        
        context += "\nRECOMENDACIONES:\n"
        recommendations = session.analysis_result.get('recommendations', [])
        for i, rec in enumerate(recommendations[:3]):  # Limit to first 3 recommendations
            context += f"- {rec.get('title', 'Sin título')}: {rec.get('description', '')}\n"
        
        if len(recommendations) > 3:
            context += f"... y {len(recommendations) - 3} recomendaciones más.\n"
        
        # Add conversation history
        context += "\nHISTORIAL DE CONVERSACIÓN:\n"
        for msg in session.conversation_history[-10:]:  # Last 10 messages
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
