#!/usr/bin/env python3
"""
Setup script for Proxy Contabilidad API
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def create_virtual_environment():
    """Create a virtual environment"""
    if os.path.exists("venv"):
        print("⚠️  Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")


def install_dependencies():
    """Install project dependencies"""
    # Determine the correct pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")


def create_env_file():
    """Create .env file from example"""
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        return True
    
    if os.path.exists("config.env.example"):
        shutil.copy("config.env.example", ".env")
        print("✅ Created .env file from example")
        print("⚠️  Please edit .env file and add your OpenAI API key")
        return True
    else:
        print("❌ config.env.example not found")
        return False


def run_tests():
    """Run basic tests"""
    # Determine the correct python command based on OS
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} test_basic.py", "Running basic tests")


def main():
    """Main setup function"""
    print("🚀 Setting up Proxy Contabilidad API...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Run tests (optional)
    print("\n🧪 Running tests...")
    run_tests()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Activate the virtual environment:")
    
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    
    print("3. Start the server:")
    print("   python main.py")
    print("4. Open http://localhost:8000 in your browser")
    print("5. Check the API documentation at http://localhost:8000/docs")


if __name__ == "__main__":
    main() 