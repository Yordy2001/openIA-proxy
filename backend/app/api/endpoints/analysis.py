from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from typing import List, Optional
from app.core.config import settings
from app.models.analysis import AnalysisResponse
from app.services.excel_service import ExcelProcessor
from app.services.session_service import session_service
from app.dependencies import get_ai_service

router = APIRouter()

# Initialize services
excel_processor = ExcelProcessor()


@router.post("/", response_model=AnalysisResponse)
async def analyze_accounting_files(
    files: List[UploadFile] = File(..., description="Archivos Excel para analizar"),
    prompt: Optional[str] = Form(None, description="Prompt personalizado para el análisis"),
    ai_svc = Depends(get_ai_service)
):
    """
    Analizar archivos contables de Excel para detectar errores en cuadres contables.
    
    - **files**: Uno o más archivos Excel (.xlsx, .xls)
    - **prompt**: Prompt personalizado opcional para el análisis
    
    Retorna un análisis estructurado con hallazgos y recomendaciones.
    """
    if not files:
        raise HTTPException(
            status_code=400,
            detail="No se proporcionaron archivos para analizar"
        )
    
    # Validate and process files
    processed_files = []
    
    for file in files:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Todos los archivos deben tener un nombre"
            )
        
        try:
            # Read file content
            content = await file.read()
            
            # Validate file
            excel_processor.validate_file(
                file.filename,
                len(content),
                settings.MAX_FILE_SIZE
            )
            
            # Store file data
            processed_files.append({
                'filename': file.filename,
                'content': content
            })
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar el archivo {file.filename}: {str(e)}"
            )
    
    try:
        # Process Excel files
        if len(processed_files) == 1:
            excel_data = excel_processor.extract_data_from_excel(
                processed_files[0]['content'],
                processed_files[0]['filename']
            )
        else:
            excel_data = excel_processor.process_multiple_files(processed_files)
        
        # Analyze with AI service
        analysis_result = ai_svc.analyze_accounting_data(
            excel_data,
            prompt or ""
        )
        
        # Create session for chat (ESTO ES LO QUE FALTABA!)
        file_names = [f["filename"] for f in processed_files]
        session_id = session_service.create_session(
            analysis_result=analysis_result.dict(),
            excel_data={"data": excel_data, "files": file_names},
            file_names=file_names
        )
        
        # Add session_id to response
        analysis_result.session_id = session_id
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar los archivos: {str(e)}"
        ) 