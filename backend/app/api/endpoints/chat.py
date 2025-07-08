from fastapi import APIRouter, HTTPException, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.services.session_service import session_service
from app.dependencies import get_ai_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_with_analysis(
    chat_request: ChatRequest,
    ai_svc = Depends(get_ai_service)
):
    """
    Chatear con el contexto de un análisis previo.
    
    - **session_id**: ID de la sesión del análisis previo
    - **message**: Mensaje del usuario
    
    Retorna la respuesta del chat con el contexto del análisis.
    """
    try:
        # Get session
        session = session_service.get_session(chat_request.session_id)
        if not session:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )
        
        # Create conversation context
        context_parts = [
            f"ANÁLISIS PREVIO: {session.analysis_result.get('summary', 'No disponible')}",
            f"ARCHIVOS ANALIZADOS: {', '.join(session.file_names)}",
            "HALLAZGOS PRINCIPALES:",
        ]
        
        # Add findings to context
        findings = session.analysis_result.get('findings', [])
        for finding in findings[:5]:  # Limit to top 5 findings
            context_parts.append(f"- {finding.get('title', 'Sin título')}: {finding.get('description', 'Sin descripción')}")
        
        # Add conversation history
        context_parts.append("CONVERSACIÓN PREVIA:")
        for msg in session.conversation_history[-5:]:  # Last 5 messages
            context_parts.append(f"{msg.role}: {msg.content}")
        
        conversation_context = "\n".join(context_parts)
        
        # Get AI response
        ai_response = ai_svc.chat_with_context(
            conversation_context,
            chat_request.message
        )
        
        # Update session with new messages
        session_service.add_message_to_session(
            chat_request.session_id,
            chat_request.message,
            ai_response
        )
        
        # Get updated session
        updated_session = session_service.get_session(chat_request.session_id)
        
        return ChatResponse(
            response=ai_response,
            session_id=chat_request.session_id,
            conversation_history=updated_session.conversation_history
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el chat: {str(e)}"
        ) 