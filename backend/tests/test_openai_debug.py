#!/usr/bin/env python3
"""
Test script to verify OpenAI service functionality
"""

import os
import json
import logging
from config import settings
from openai_service import OpenAIService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai_connection():
    """Test basic OpenAI connection"""
    print("=== Testing OpenAI Connection ===")
    
    # Check if API key is set
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "tu_openai_api_key_aqui":
        print("❌ OPENAI_API_KEY is not set properly in .env file")
        print("Please set your actual OpenAI API key in the .env file")
        return False
    
    print(f"✅ API Key found: {settings.OPENAI_API_KEY[:10]}...")
    print(f"✅ Model: {settings.OPENAI_MODEL}")
    print(f"✅ Base URL: {settings.OPENAI_BASE_URL}")
    
    try:
        # Initialize service
        service = OpenAIService()
        print("✅ Service initialized")
        
        # Test connection
        if service.test_connection():
            print("✅ Connection test passed")
            return True
        else:
            print("❌ Connection test failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def test_simple_analysis():
    """Test a simple analysis with minimal data"""
    print("\n=== Testing Simple Analysis ===")
    
    try:
        service = OpenAIService()
        
        # Simple test data (formato que espera OpenAI service)
        test_data = """
=== ANÁLISIS DE ARCHIVO: test.xlsx ===

--- HOJA: Sheet1 ---
Dimensiones: 4 filas x 3 columnas

Datos:
Fila 1: Col1: Concepto | Col2: Debe | Col3: Haber
Fila 2: Col1: Ventas | Col2: 0 | Col3: 1000
Fila 3: Col1: Caja | Col2: 1000 | Col3: 0
Fila 4: Col1: Total | Col2: 1000 | Col3: 1000

Resumen estadístico para columnas numéricas:
  Columna 2: Suma=1000.00, Promedio=500.00, Min=0.00, Max=1000.00
  Columna 3: Suma=1000.00, Promedio=500.00, Min=0.00, Max=1000.00
        """
        
        print("📊 Testing with simple accounting data...")
        result = service.analyze_accounting_data(test_data, "Analiza este cuadre contable simple")
        
        print(f"✅ Analysis result: {result.success}")
        print(f"📝 Summary: {result.summary}")
        print(f"🔍 Findings: {len(result.findings)}")
        print(f"💡 Recommendations: {len(result.recommendations)}")
        
        if result.error:
            print(f"❌ Error: {result.error}")
        
        # Show some details
        if result.findings:
            print("\n📋 Sample findings:")
            for i, finding in enumerate(result.findings[:2]):  # Show first 2
                print(f"  {i+1}. {finding.title} ({finding.severity})")
                print(f"     {finding.description[:100]}...")
                
        if result.recommendations:
            print("\n💡 Sample recommendations:")
            for i, rec in enumerate(result.recommendations[:2]):  # Show first 2
                print(f"  {i+1}. {rec.title} ({rec.priority})")
                print(f"     {rec.description[:100]}...")
            
        return result.success
        
    except Exception as e:
        print(f"❌ Error in simple analysis: {e}")
        return False

def test_with_problematic_data():
    """Test with data that should trigger findings"""
    print("\n=== Testing with Problematic Data ===")
    
    try:
        service = OpenAIService()
        
        # Test data with accounting errors
        problematic_data = """
=== ANÁLISIS DE ARCHIVO: cierre-con-errores.xlsx ===

--- HOJA: Balance ---
Dimensiones: 5 filas x 3 columnas

Datos:
Fila 1: Col1: Concepto | Col2: Debe | Col3: Haber
Fila 2: Col1: Ventas | Col2: 0 | Col3: 1000
Fila 3: Col1: Caja | Col2: 800 | Col3: 0
Fila 4: Col1: Gastos | Col2: 150 | Col3: 0
Fila 5: Col1: Total | Col2: 950 | Col3: 1000

Resumen estadístico para columnas numéricas:
  Columna 2: Suma=950.00, Promedio=475.00, Min=0.00, Max=800.00
  Columna 3: Suma=1000.00, Promedio=500.00, Min=0.00, Max=1000.00
        """
        
        print("📊 Testing with problematic accounting data...")
        result = service.analyze_accounting_data(problematic_data, "Detecta errores en este cuadre contable")
        
        print(f"✅ Analysis result: {result.success}")
        print(f"📝 Summary: {result.summary}")
        print(f"🔍 Findings: {len(result.findings)}")
        print(f"💡 Recommendations: {len(result.recommendations)}")
        
        if result.findings:
            print("\n📋 Detected issues:")
            for i, finding in enumerate(result.findings):
                print(f"  {i+1}. [{finding.severity.upper()}] {finding.title}")
                print(f"     Location: {finding.location}")
                print(f"     Fix: {finding.suggested_fix}")
                print()
                
        return result.success
        
    except Exception as e:
        print(f"❌ Error in problematic data analysis: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 Testing OpenAI Service Integration")
    print("=" * 50)
    
    # Test 1: Connection
    connection_ok = test_openai_connection()
    
    if connection_ok:
        # Test 2: Simple analysis
        simple_ok = test_simple_analysis()
        
        if simple_ok:
            # Test 3: Problematic data
            problematic_ok = test_with_problematic_data()
            
            if problematic_ok:
                print("\n🎉 All tests passed! OpenAI service is working correctly.")
                print("\n✅ Ready to test the /analyze endpoint with real Excel files!")
            else:
                print("\n⚠️  Problematic data test failed - check logs for details")
        else:
            print("\n⚠️  Simple analysis test failed - check logs for details")
    else:
        print("\n❌ Connection test failed - check API key and internet connection")
        print("\n📋 Steps to fix:")
        print("1. Create .env file with OPENAI_API_KEY")
        print("2. Get API key from https://platform.openai.com/api-keys")
        print("3. Set AI_PROVIDER=openai in .env file")

if __name__ == "__main__":
    main() 