import openai
import json
import re
from typing import Dict, Any
from fastapi import HTTPException
from config import settings
from models import AnalysisResponse, Finding


class OpenAIService:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada en las variables de entorno")
        
        self.client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
        self.model = settings.OPENAI_MODEL
    
    def analyze_accounting_data(self, excel_data: str, custom_prompt: str = None) -> AnalysisResponse:
        """Send accounting data to OpenAI for analysis"""
        try:
            # Prepare the prompt
            system_prompt = custom_prompt if custom_prompt else settings.DEFAULT_PROMPT
            
            # Combine system prompt with data
            full_prompt = f"{system_prompt}\n\n--- DATOS CONTABLES ---\n{excel_data}"
            
            # Add JSON format instruction
            json_instruction = """

IMPORTANTE: Responde ÚNICAMENTE con un objeto JSON válido con la siguiente estructura:
{
    "summary": "Resumen general del análisis",
    "findings": [
        {
            "sheet": "Nombre de la hoja",
            "row": número_de_fila_o_null,
            "description": "Descripción detallada del hallazgo"
        }
    ],
    "recommendations": "Recomendaciones para resolver los problemas encontrados"
}

NO incluyas texto adicional fuera del JSON. Solo responde con el JSON."""
            
            full_prompt += json_instruction
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract the response content
            response_content = response.choices[0].message.content.strip()
            
            # Parse the JSON response
            try:
                analysis_data = json.loads(response_content)
                return self._parse_analysis_response(analysis_data)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from the response
                json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
                if json_match:
                    try:
                        analysis_data = json.loads(json_match.group())
                        return self._parse_analysis_response(analysis_data)
                    except json.JSONDecodeError:
                        pass
                
                # If still can't parse, create a fallback response
                return AnalysisResponse(
                    summary="Análisis completado, pero hubo un problema con el formato de respuesta.",
                    findings=[
                        Finding(
                            sheet="General",
                            row=None,
                            description=f"Respuesta del análisis: {response_content[:500]}..."
                        )
                    ],
                    recommendations="Revisar manualmente la respuesta completa del análisis."
                )
        
        except openai.APIError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Error en la API de OpenAI: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar la respuesta de OpenAI: {str(e)}"
            )
    
    def _parse_analysis_response(self, analysis_data: Dict[str, Any]) -> AnalysisResponse:
        """Parse the analysis response from OpenAI into structured format"""
        try:
            # Extract findings
            findings = []
            if 'findings' in analysis_data and isinstance(analysis_data['findings'], list):
                for finding_data in analysis_data['findings']:
                    if isinstance(finding_data, dict):
                        finding = Finding(
                            sheet=finding_data.get('sheet', 'General'),
                            row=finding_data.get('row'),
                            description=finding_data.get('description', 'No description provided')
                        )
                        findings.append(finding)
            
            # Create the response object
            return AnalysisResponse(
                summary=analysis_data.get('summary', 'Análisis completado'),
                findings=findings,
                recommendations=analysis_data.get('recommendations', 'No se proporcionaron recomendaciones específicas')
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al parsear la respuesta del análisis: {str(e)}"
            )
    
    def test_connection(self) -> bool:
        """Test the OpenAI API connection"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception:
            return False 