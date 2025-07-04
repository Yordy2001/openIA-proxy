"""
Google Gemini service for analyzing accounting data
"""

import json
import google.generativeai as genai
from typing import Dict, Any, Optional
import logging
from models import AnalysisResponse, Finding, Recommendation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google Gemini AI"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """Initialize Gemini service"""
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        
        try:
            # Configure the API
            genai.configure(api_key=api_key)
            
            # Initialize model
            self.model = genai.GenerativeModel(model_name)
            
            if self.model is None:
                raise ValueError(f"Failed to initialize Gemini model: {model_name}")
                
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {e}")
            raise ValueError(f"Gemini initialization failed: {e}")
        
        # Configure safety settings
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    
    def test_connection(self) -> bool:
        """Test the connection to Gemini"""
        try:
            if self.model is None:
                return False
                
            # Simple test generation
            response = self.model.generate_content(
                "Responde con: 'Conexión exitosa'",
                safety_settings=self.safety_settings
            )
            # Handle complex response structure
            response_text = self._extract_response_text(response)
            return "exitosa" in response_text.lower()
        except Exception as e:
            logger.error(f"Error testing Gemini connection: {e}")
            return False
    
    def analyze_accounting_data(self, excel_data: Any, custom_prompt: str = "") -> AnalysisResponse:
        """
        Analyze accounting data using Gemini
        
        Args:
            excel_data: Dictionary containing Excel data
            custom_prompt: Optional custom prompt
            
        Returns:
            AnalysisResponse with findings and recommendations
        """
        try:
            if self.model is None:
                raise ValueError("Gemini model is not initialized")
                
            # Create analysis prompt
            prompt = self._create_analysis_prompt(excel_data, custom_prompt)
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    top_p=0.8,
                    max_output_tokens=2048,
                )
            )
            
            # Parse response
            response_text = self._extract_response_text(response)
            analysis_result = self._parse_gemini_response(response_text)
            
            logger.info(f"Analysis completed successfully with {len(analysis_result.findings)} findings")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing data with Gemini: {e}")
            
            # Return error response
            return AnalysisResponse(
                success=False,
                error=f"Error en el análisis: {str(e)}",
                findings=[],
                recommendations=[],
                summary="Error al procesar el análisis",
                metadata={
                    "provider": "gemini",
                    "model": self.model_name,
                    "error": str(e)
                }
            )
    
    def _extract_response_text(self, response) -> str:
        """
        Extract text from Gemini response, handling complex response structures
        
        Args:
            response: Gemini response object
            
        Returns:
            str: Extracted text content
        """
        # Check if response is None or empty
        if response is None:
            logger.error("Response is None")
            return "Error: Response is None"
        
        try:
            # Try simple text accessor first
            if hasattr(response, 'text'):
                response_text = response.text
                if response_text:
                    return response_text
                else:
                    logger.warning("response.text is empty")
        except Exception as e:
            logger.info(f"Failed to access response.text: {e}")
            
        try:
            # Try accessing via candidates and parts
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        # Combine all parts
                        text_parts = []
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(part.text)
                        combined_text = ''.join(text_parts)
                        if combined_text:
                            return combined_text
        except Exception as e:
            logger.error(f"Error extracting text from response parts: {e}")
            
        try:
            # Try accessing via response.parts directly
            if hasattr(response, 'parts') and response.parts:
                text_parts = []
                for part in response.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
                combined_text = ''.join(text_parts)
                if combined_text:
                    return combined_text
        except Exception as e:
            logger.error(f"Error extracting text from response.parts: {e}")
            
        try:
            # Try using resolve() method if available
            if hasattr(response, 'resolve'):
                resolved = response.resolve()
                if hasattr(resolved, 'text'):
                    return resolved.text
        except Exception as e:
            logger.error(f"Error resolving response: {e}")
            
        # If all else fails, return error message
        logger.error("Unable to extract text from response using any method")
        return "Error: Unable to extract response text"

    def _create_analysis_prompt(self, excel_data: Any, custom_prompt: str = "") -> str:
        """Create the analysis prompt for Gemini"""
        
        # Handle both string and dict data formats
        if isinstance(excel_data, str):
            # Excel data is already formatted as a string
            data_section = excel_data
        else:
            # Excel data is a dictionary, serialize it
            data_section = json.dumps(excel_data, indent=2, default=str)
        
        base_prompt = f"""
        Eres un experto contador y auditor especializado en análisis de cuadres contables.
        
        Analiza los siguientes datos de Excel y detecta posibles errores en cuadres contables:
        
        DATOS DEL ARCHIVO:
        {data_section}
        
        INSTRUCCIONES:
        1. Busca inconsistencias en sumas, balances y cuadres
        2. Identifica errores de cálculo o fórmulas
        3. Detecta valores faltantes o anómalos
        4. Revisa la coherencia entre diferentes hojas o tablas
        5. Verifica que los debitos y créditos cuadren
        
        {'INSTRUCCIONES ADICIONALES: ' + custom_prompt if custom_prompt else ''}
        
        IMPORTANTE: Responde ÚNICAMENTE con un JSON válido en el siguiente formato:
        {{
            "success": true,
            "findings": [
                {{
                    "type": "error|warning|info",
                    "title": "Título del hallazgo",
                    "description": "Descripción detallada",
                    "location": "Ubicación en el archivo",
                    "severity": "high|medium|low",
                    "suggested_fix": "Sugerencia de corrección"
                }}
            ],
            "recommendations": [
                {{
                    "title": "Título de recomendación",
                    "description": "Descripción de la recomendación",
                    "priority": "high|medium|low",
                    "category": "calculation|format|process|validation"
                }}
            ],
            "summary": "Resumen ejecutivo del análisis",
            "metadata": {{
                "total_findings": 0,
                "critical_issues": 0,
                "sheets_analyzed": 0
            }}
        }}
        """
        
        return base_prompt
    
    def _parse_gemini_response(self, response_text: str) -> AnalysisResponse:
        """Parse Gemini response into structured format"""
        try:
            # Clean response text
            response_text = response_text.strip()
            
            # Check if response is empty or contains error messages
            if not response_text:
                logger.error("Response text is empty")
                return self._create_fallback_response("Response text is empty")
            
            if response_text.startswith("Error:"):
                logger.error(f"Response contains error: {response_text}")
                return self._create_fallback_response(response_text)
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            data = json.loads(response_text)
            
            # Convert to structured response
            findings = []
            for finding_data in data.get("findings", []):
                finding = Finding(
                    type=finding_data.get("type", "info"),
                    title=finding_data.get("title", ""),
                    description=finding_data.get("description", ""),
                    location=finding_data.get("location", ""),
                    severity=finding_data.get("severity", "medium"),
                    suggested_fix=finding_data.get("suggested_fix", "")
                )
                findings.append(finding)
            
            recommendations = []
            for rec_data in data.get("recommendations", []):
                recommendation = Recommendation(
                    title=rec_data.get("title", ""),
                    description=rec_data.get("description", ""),
                    priority=rec_data.get("priority", "medium"),
                    category=rec_data.get("category", "general")
                )
                recommendations.append(recommendation)
            
            return AnalysisResponse(
                success=data.get("success", True),
                findings=findings,
                recommendations=recommendations,
                summary=data.get("summary", "Análisis completado"),
                metadata={
                    "provider": "gemini",
                    "model": self.model_name,
                    **data.get("metadata", {})
                }
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Gemini JSON response: {e}")
            logger.error(f"Response text: {response_text}")
            
            # Return fallback response
            return AnalysisResponse(
                success=False,
                error="Error al parsear la respuesta de Gemini",
                findings=[],
                recommendations=[],
                summary="Error en el procesamiento de la respuesta",
                metadata={
                    "provider": "gemini",
                    "model": self.model_name,
                    "parse_error": str(e)
                }
            )
        
        except Exception as e:
            logger.error(f"Unexpected error parsing Gemini response: {e}")
            return AnalysisResponse(
                success=False,
                error=f"Error inesperado: {str(e)}",
                findings=[],
                recommendations=[],
                summary="Error inesperado en el análisis",
                metadata={
                    "provider": "gemini",
                    "model": self.model_name,
                    "error": str(e)
                }
            )
    
    def _create_fallback_response(self, error_message: str) -> AnalysisResponse:
        """Create a fallback response when parsing fails"""
        return AnalysisResponse(
            success=False,
            error=f"Error al procesar la respuesta: {error_message}",
            findings=[
                Finding(
                    type="error",
                    title="Error de procesamiento",
                    description="No se pudo procesar la respuesta del modelo de IA. Esto puede deberse a un problema de conectividad o formato de respuesta.",
                    location="Sistema",
                    severity="high",
                    suggested_fix="Intente nuevamente con un archivo más pequeño o verifique la conexión a internet."
                )
            ],
            recommendations=[
                Recommendation(
                    title="Reintentar análisis",
                    description="Pruebe subir el archivo nuevamente o use un archivo de Excel más pequeño.",
                    priority="high",
                    category="process"
                )
            ],
            summary="Error al procesar la respuesta del modelo de IA",
            metadata={
                "provider": "gemini",
                "model": self.model_name,
                "error": error_message
            }
        ) 