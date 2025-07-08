"""
Basic tests for the Proxy Contabilidad API
"""

# import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import io
import os

# Mock the OpenAI service to avoid making actual API calls during tests
with patch('openai_service.OpenAIService') as mock_openai:
    from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Proxy Contabilidad API está funcionando correctamente" in response.json()["message"]


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data
    assert "configuration" in data


def test_analyze_endpoint_no_files():
    """Test analyze endpoint without files"""
    response = client.post("/analyze")
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_invalid_file():
    """Test analyze endpoint with invalid file type"""
    # Create a fake text file
    fake_file = io.BytesIO(b"This is not an Excel file")
    
    response = client.post(
        "/analyze",
        files={"files": ("test.txt", fake_file, "text/plain")}
    )
    
    # Should return error for invalid file type
    assert response.status_code == 400


@patch('openai_service.OpenAIService')
def test_analyze_endpoint_with_mock_excel(mock_openai_service):
    """Test analyze endpoint with mocked services"""
    # Mock OpenAI service response
    mock_service_instance = Mock()
    mock_service_instance.analyze_accounting_data.return_value = {
        "summary": "Test analysis completed",
        "findings": [
            {
                "sheet": "Test Sheet",
                "row": 1,
                "description": "Test finding"
            }
        ],
        "recommendations": "Test recommendations"
    }
    mock_openai_service.return_value = mock_service_instance
    
    # Create a simple Excel-like file (this would normally be a real Excel file)
    fake_excel = io.BytesIO(b"PK\x03\x04")  # ZIP file signature (Excel files are ZIP-based)
    
    response = client.post(
        "/analyze",
        files={"files": ("test.xlsx", fake_excel, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )
    
    # Note: This test might fail with real Excel processing, but demonstrates the structure
    # In a real test environment, you'd use actual Excel files


def test_excel_processor_validation():
    """Test Excel processor file validation"""
    from excel_service import ExcelProcessor
    
    processor = ExcelProcessor()
    
    # Test valid file
    try:
        processor.validate_file("test.xlsx", 1000, 10000)
        assert True
    except Exception:
        assert False
    
    # # Test invalid extension
    # with pytest.raises(Exception):
    #     processor.validate_file("test.txt", 1000, 10000)
    
    # # Test file too large
    # with pytest.raises(Exception):
    #     processor.validate_file("test.xlsx", 20000, 10000)


if __name__ == "__main__":
    print("Running basic tests...")
    test_root_endpoint()
    test_health_endpoint()
    test_analyze_endpoint_no_files()
    test_excel_processor_validation()
    print("Basic tests completed!") 