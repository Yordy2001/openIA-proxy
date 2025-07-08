import pandas as pd
import openpyxl
from typing import List, Dict, Any
import io
import os
from fastapi import HTTPException


class ExcelProcessor:
    def __init__(self):
        self.supported_extensions = {'.xlsx', '.xls'}
    
    def validate_file(self, filename: str, file_size: int, max_size: int) -> bool:
        """Validate if the file is supported and within size limits"""
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext not in self.supported_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Formato de archivo no soportado. Formatos permitidos: {', '.join(self.supported_extensions)}"
            )
        
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"Archivo demasiado grande. Tamaño máximo: {max_size / (1024*1024):.1f}MB"
            )
        
        return True
    
    def extract_data_from_excel(self, file_content: bytes, filename: str) -> str:
        """Extract and format data from Excel file"""
        try:
            # Read Excel file
            excel_file = pd.ExcelFile(io.BytesIO(file_content))
            
            formatted_data = []
            formatted_data.append(f"=== ANÁLISIS DE ARCHIVO: {filename} ===\n")
            
            # Process each sheet
            for sheet_name in excel_file.sheet_names:
                formatted_data.append(f"\n--- HOJA: {sheet_name} ---")
                
                try:
                    # Read the sheet
                    df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
                    
                    # Remove completely empty rows and columns
                    df = df.dropna(how='all').dropna(axis=1, how='all')
                    
                    if df.empty:
                        formatted_data.append("Esta hoja está vacía o no contiene datos válidos.")
                        continue
                    
                    # Add sheet information
                    formatted_data.append(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
                    
                    # Convert to string representation
                    formatted_data.append("\nDatos:")
                    
                    # Process each row with row numbers
                    for idx, row in df.iterrows():
                        row_data = []
                        for col_idx, value in enumerate(row):
                            if pd.notna(value):
                                # Format numbers appropriately
                                if isinstance(value, (int, float)):
                                    if isinstance(value, float) and value.is_integer():
                                        formatted_value = f"{int(value)}"
                                    else:
                                        formatted_value = f"{value:,.2f}"
                                else:
                                    formatted_value = str(value)
                                row_data.append(f"Col{col_idx+1}: {formatted_value}")
                        
                        if row_data:
                            formatted_data.append(f"Fila {idx+1}: {' | '.join(row_data)}")
                    
                    # Add summary statistics for numeric columns
                    numeric_columns = df.select_dtypes(include=['number']).columns
                    if len(numeric_columns) > 0:
                        formatted_data.append(f"\nResumen estadístico para columnas numéricas:")
                        for col in numeric_columns:
                            col_data = df[col].dropna()
                            if len(col_data) > 0:
                                formatted_data.append(
                                    f"  Columna {col+1}: Suma={col_data.sum():,.2f}, "
                                    f"Promedio={col_data.mean():,.2f}, "
                                    f"Min={col_data.min():,.2f}, "
                                    f"Max={col_data.max():,.2f}"
                                )
                    
                except Exception as e:
                    formatted_data.append(f"Error al procesar la hoja '{sheet_name}': {str(e)}")
                    continue
            
            return "\n".join(formatted_data)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar el archivo Excel: {str(e)}"
            )
    
    def process_multiple_files(self, files_data: List[Dict[str, Any]]) -> str:
        """Process multiple Excel files and combine their data"""
        all_data = []
        
        for file_data in files_data:
            filename = file_data['filename']
            content = file_data['content']
            
            try:
                file_analysis = self.extract_data_from_excel(content, filename)
                all_data.append(file_analysis)
                all_data.append("\n" + "="*80 + "\n")
            except Exception as e:
                all_data.append(f"Error procesando {filename}: {str(e)}")
                all_data.append("\n" + "="*80 + "\n")
        
        return "\n".join(all_data) 