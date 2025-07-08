from fastapi import APIRouter, HTTPException
from app.models.chat import SessionListResponse
from app.services.session_service import session_service

router = APIRouter()


@router.get("/", response_model=SessionListResponse)
async def list_sessions():
    """
    Listar todas las sesiones de análisis.
    
    Retorna una lista de sesiones con información básica.
    """
    try:
        sessions = session_service.list_sessions()
        return SessionListResponse(
            sessions=sessions,
            total=len(sessions)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar sesiones: {str(e)}"
        )


@router.get("/{session_id}")
async def get_session_details(session_id: str):
    """
    Obtener detalles de una sesión específica.
    
    - **session_id**: ID de la sesión
    
    Retorna los detalles completos de la sesión.
    """
    try:
        session = session_service.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )
        
        return {
            "session_id": session.session_id,
            "analysis_result": session.analysis_result,
            "conversation_history": session.conversation_history,
            "created_at": session.created_at,
            "last_activity": session.last_activity,
            "file_names": session.file_names
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener sesión: {str(e)}"
        )


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """
    Eliminar una sesión específica.
    
    - **session_id**: ID de la sesión
    
    Retorna confirmación de eliminación.
    """
    try:
        success = session_service.delete_session(session_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )
        
        return {"message": f"Sesión {session_id} eliminada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar sesión: {str(e)}"
        ) 