import openai
import json
import re
import logging
from typing import Dict, Any
from fastapi import HTTPException
from config import settings
from models import AnalysisResponse, Finding, Recommendation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada en las variables de entorno")
        
        # Initialize client (use default endpoint)
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    def test_connection(self) -> bool:
        """Test the OpenAI API connection"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Responde con: 'Conexión exitosa'"}],
                max_tokens=10
            )
            message_content = response.choices[0].message.content
            if message_content is None:
                return False
            response_text = message_content.strip()
            return "exitosa" in response_text.lower()
        except Exception as e:
            logger.error(f"Error testing OpenAI connection: {e}")
            return False
    
    def analyze_accounting_data(self, excel_data: str, custom_prompt: str = "") -> AnalysisResponse:
        """Send accounting data to OpenAI for analysis"""
        try:
            # Create the analysis prompt
            prompt = self._create_analysis_prompt(excel_data, custom_prompt or "")
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=2048
            )
            
            # Extract the response content
            message_content = response.choices[0].message.content
            if message_content is None:
                raise ValueError("OpenAI response content is None")
            response_content = message_content.strip()
            
            # Parse the response
            analysis_result = self._parse_openai_response(response_content)
            
            logger.info(f"Analysis completed successfully with {len(analysis_result.findings)} findings")
            return analysis_result
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return AnalysisResponse(
                success=False,
                error=f"Error en la API de OpenAI: {str(e)}",
                findings=[],
                recommendations=[],
                summary="Error al procesar el análisis",
                metadata={
                    "provider": "openai",
                    "model": self.model,
                    "error": str(e)
                }
            )
        except Exception as e:
            logger.error(f"Error analyzing data with OpenAI: {e}")
            return AnalysisResponse(
                success=False,
                error=f"Error al procesar la respuesta de OpenAI: {str(e)}",
                findings=[],
                recommendations=[],
                summary="Error al procesar el análisis",
                metadata={
                    "provider": "openai",
                    "model": self.model,
                    "error": str(e)
                }
            )
    
    def _create_analysis_prompt(self, excel_data: str, custom_prompt: str = "") -> str:
        """Create the analysis prompt for OpenAI"""
        
        base_prompt = f"""
        Eres un experto contador y auditor especializado en análisis de cuadres contables.
        
        Analiza los siguientes datos de Excel y detecta posibles errores en cuadres contables:
        
        DATOS DEL ARCHIVO:
        {excel_data}
        
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
    
    def _parse_openai_response(self, response_text: str) -> AnalysisResponse:
        """Parse OpenAI response into structured format"""
        try:
            # Clean response text
            response_text = response_text.strip()
            
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
                    "provider": "openai",
                    "model": self.model,
                    **data.get("metadata", {})
                }
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing OpenAI JSON response: {e}")
            logger.error(f"Response text: {response_text}")
            
            # Return fallback response
            return AnalysisResponse(
                success=False,
                error="Error al parsear la respuesta de OpenAI",
                findings=[],
                recommendations=[],
                summary="Error en el procesamiento de la respuesta",
                metadata={
                    "provider": "openai",
                    "model": self.model,
                    "parse_error": str(e)
                }
            )
        
        except Exception as e:
            logger.error(f"Unexpected error parsing OpenAI response: {e}")
            return AnalysisResponse(
                success=False,
                error=f"Error inesperado: {str(e)}",
                findings=[],
                recommendations=[],
                summary="Error inesperado en el análisis",
                metadata={
                    "provider": "openai",
                    "model": self.model,
                    "error": str(e)
                }
            ) 
    def chat_with_context(self, conversation_context: str, user_message: str) -> str:
        """Chat with user using the analysis context"""
        try:
            # Create the chat prompt
            prompt = f"""
            Eres un experto contador y auditor especializado en análisis de cuadres contables.
            
            CONTEXTO DEL ANÁLISIS PREVIO:
            {conversation_context}
            
            INSTRUCCIONES:
            - Responde a la pregunta del usuario basándote en el análisis previo
            - Sé específico y usa la información del análisis
            - Si la pregunta no está relacionada con el análisis, redirige al usuario
            - Mantén un tono profesional pero amigable
            - Proporciona explicaciones claras y detalladas
            
            PREGUNTA DEL USUARIO:
            {user_message}
            
            RESPUESTA:
            """
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1024
            )
            
            # Extract the response content
            message_content = response.choices[0].message.content
            if message_content is None:
                raise ValueError("OpenAI response content is None")
            
            return message_content.strip()
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error in chat: {e}")
            return f"Lo siento, ocurrió un error al procesar tu pregunta: {str(e)}"
        except Exception as e:
            logger.error(f"Error in chat with OpenAI: {e}")
            return f"Lo siento, ocurrió un error inesperado: {str(e)}"
