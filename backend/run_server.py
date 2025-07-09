#!/usr/bin/env python3
"""
Script para ejecutar el servidor FastAPI
"""

import sys
import os
import uvicorn

# Asegurar que estamos en el directorio correcto
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Agregar el directorio actual al path
sys.path.insert(0, current_dir)

try:
    print("🚀 Iniciando servidor FastAPI...")
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"📂 Archivos en directorio: {os.listdir('.')}")
    
    # Verificar que los archivos necesarios existen
    required_files = ['main.py', 'models.py', 'excel_service.py', 'config.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {missing_files}")
        sys.exit(1)
    
    print("✅ Todos los archivos necesarios están presentes")
    
    # Intentar importar el app
    print("📦 Importando aplicación...")
    from main import app
    print("✅ Aplicación importada exitosamente")
    
    # Ejecutar el servidor
    print("🌐 Iniciando servidor en http://localhost:7000")
    print("🔧 Presiona Ctrl+C para detener el servidor")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7000,
        log_level="info",
        reload=False  # Disable reload for stability
    )
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("🔍 Verificando dependencias...")
    
    # Verificar dependencias básicas
    try:
        import fastapi
        print("✅ FastAPI disponible")
    except ImportError:
        print("❌ FastAPI no disponible")
    
    try:
        import pandas
        print("✅ Pandas disponible")
    except ImportError:
        print("❌ Pandas no disponible")
        
    try:
        import openpyxl
        print("✅ OpenPyXL disponible")
    except ImportError:
        print("❌ OpenPyXL no disponible")
    
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 