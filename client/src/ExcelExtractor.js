import React, { useState } from 'react';
import apiService from './apiService';
import ExcelTable from './ExcelTable';

const ExcelExtractor = () => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [structuredData, setStructuredData] = useState(null);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragOver(false);
    
    const droppedFile = event.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setError(null);
    }
  };

  const isExcelFile = (file) => {
    const allowedTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/vnd.ms-excel',
      'application/vnd.ms-excel.sheet.macroEnabled.12'
    ];
    return allowedTypes.includes(file.type) || file.name.endsWith('.xlsx') || file.name.endsWith('.xls');
  };

  const handleExtract = async () => {
    if (!file) {
      setError('Por favor selecciona un archivo Excel');
      return;
    }

    if (!isExcelFile(file)) {
      setError('El archivo seleccionado no es un archivo Excel válido');
      return;
    }

    setIsLoading(true);
    setError(null);
    setStructuredData(null);

    try {
      const data = await apiService.extractExcelData(file);
      setStructuredData(data);
    } catch (err) {
      setError(err.message || 'Error al extraer los datos del archivo');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDataChange = (newData) => {
    setStructuredData(newData);
  };

  const handleReset = () => {
    setFile(null);
    setStructuredData(null);
    setError(null);
  };

  return (
    <div className="excel-extractor">
      <div className="extractor-header">
        <h2>📊 Extractor de Datos Excel</h2>
        <p>Sube un archivo Excel para visualizar y editar sus datos en una tabla interactiva</p>
      </div>

      {!structuredData ? (
        <div className="upload-section">
          <div 
            className={`file-input ${dragOver ? 'drag-over' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileChange}
              disabled={isLoading}
              style={{ display: 'none' }}
              id="excel-file-input"
            />
            <label htmlFor="excel-file-input" style={{ cursor: 'pointer', display: 'block' }}>
              <div style={{ padding: '40px', textAlign: 'center' }}>
                <div style={{ fontSize: '48px', marginBottom: '20px' }}>📁</div>
                {file ? (
                  <div>
                    <p style={{ color: '#28a745', fontWeight: 'bold' }}>
                      ✅ Archivo seleccionado: {file.name}
                    </p>
                    <p style={{ color: '#666', fontSize: '14px' }}>
                      Tamaño: {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                ) : (
                  <div>
                    <p style={{ fontSize: '18px', marginBottom: '10px' }}>
                      Arrastra un archivo Excel aquí o haz clic para seleccionarlo
                    </p>
                    <p style={{ color: '#666', fontSize: '14px' }}>
                      Formatos soportados: .xlsx, .xls
                    </p>
                  </div>
                )}
              </div>
            </label>
          </div>

          {error && (
            <div style={{ 
              color: 'red', 
              padding: '15px', 
              backgroundColor: '#ffebee', 
              borderRadius: '4px',
              marginTop: '20px'
            }}>
              ❌ {error}
            </div>
          )}

          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <button
              onClick={handleExtract}
              disabled={!file || isLoading}
              className="button"
              style={{ 
                backgroundColor: '#007bff',
                fontSize: '16px',
                padding: '12px 24px'
              }}
            >
              {isLoading ? '⏳ Extrayendo datos...' : '📊 Extraer Datos'}
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div style={{ marginBottom: '20px', textAlign: 'center' }}>
            <button 
              onClick={handleReset} 
              className="button"
              style={{ backgroundColor: '#6c757d' }}
            >
              🔄 Subir Otro Archivo
            </button>
          </div>
          
          <ExcelTable 
            structuredData={structuredData}
            onDataChange={handleDataChange}
          />
        </div>
      )}

      {/* Loading indicator */}
      {isLoading && (
        <div className="loading" style={{ marginTop: '20px' }}>
          <div className="spinner"></div>
          <p>Extrayendo datos del archivo Excel...</p>
        </div>
      )}

      {/* Features info */}
      {!structuredData && (
        <div style={{ marginTop: '40px', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
          <h3>🎯 Características:</h3>
          <ul style={{ textAlign: 'left', display: 'inline-block' }}>
            <li>✅ Visualización de datos en tabla interactiva</li>
            <li>✅ Edición de celdas con doble clic</li>
            <li>✅ Soporte para múltiples hojas</li>
            <li>✅ Identificación automática de columnas numéricas</li>
            <li>✅ Descarga del archivo modificado</li>
            <li>✅ Interfaz intuitiva y responsive</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ExcelExtractor; 