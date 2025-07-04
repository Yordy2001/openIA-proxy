#!/usr/bin/env python3
"""
Quick start script for Proxy Contabilidad API
"""

import os
import sys
from pathlib import Path

def main():
    """Quick start the application"""
    print("🚀 Starting Proxy Contabilidad API...")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("Please run setup.py first or create .env file with your API key")
        print("Example:")
        print("AI_PROVIDER=gemini")
        print("GEMINI_API_KEY=your_api_key_here")
        print("# or")
        print("AI_PROVIDER=openai")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Check for virtual environment
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found!")
        print("Please run setup.py first or create a virtual environment")
        sys.exit(1)
    
    print("✅ Starting server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Alternative docs: http://localhost:8000/redoc")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Import and run the app
    try:
        import uvicorn
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError:
        print("❌ Dependencies not installed!")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 