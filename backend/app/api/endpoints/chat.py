from fastapi import APIRouter, HTTPException, Depends
from app.models.chat import ChatRequest, ChatResponse
from chat_models import ChatMessage
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
        
        # Add user message to conversation
        user_message = ChatMessage(
            role="user",
            content=chat_request.message
        )
        session_service.add_message(chat_request.session_id, user_message)
        
        # Get conversation context using the improved method
        context = session_service.get_conversation_context(chat_request.session_id)
        
        # Get AI response
        ai_response = ai_svc.chat_with_context(
            context,
            chat_request.message
        )
        
        # Add AI response to conversation
        ai_message = ChatMessage(
            role="assistant",
            content=ai_response
        )
        session_service.add_message(chat_request.session_id, ai_message)
        
        # Get updated session for response
        updated_session = session_service.get_session(chat_request.session_id)
        
        # Convert messages to expected format or provide empty list
        conversation_history = []
        if updated_session and updated_session.conversation_history:
            # Convert to the expected format
            from app.models.chat import ChatMessage as AppChatMessage
            conversation_history = [
                AppChatMessage(role=msg.role, content=msg.content)
                for msg in updated_session.conversation_history
            ]
        
        # Return response
        return ChatResponse(
            response=ai_response,
            session_id=chat_request.session_id,
            conversation_history=conversation_history
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el chat: {str(e)}"
        ) 