import React, { useState, useRef } from 'react';
import apiService from '../services/api';

const FileUpload = ({ onAnalysisComplete, onAnalysisError, onLoadingChange, loading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [customPrompt, setCustomPrompt] = useState('');
  const fileInputRef = useRef(null);

  const validateFiles = (files) => {
    const allowedTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/vnd.ms-excel',
      '.xlsx',
      '.xls'
    ];
    
    const maxSize = 10 * 1024 * 1024; // 10MB
    
    for (let file of files) {
      // Check file type
      if (!allowedTypes.includes(file.type) && 
          !file.name.endsWith('.xlsx') && 
          !file.name.endsWith('.xls')) {
        return { valid: false, error: 'Solo se permiten archivos Excel (.xlsx, .xls)' };
      }
      
      // Check file size
      if (file.size > maxSize) {
        return { valid: false, error: `El archivo ${file.name} es muy grande (máximo 10MB)` };
      }
    }
    
    return { valid: true };
  };

  const handleFiles = async (files) => {
    if (!files || files.length === 0) return;

    const validation = validateFiles(files);
    if (!validation.valid) {
      onAnalysisError(validation.error);
      return;
    }

    try {
      onLoadingChange(true);
      const results = await apiService.analyzeFiles(files, customPrompt);
      onAnalysisComplete(results);
    } catch (error) {
      onAnalysisError(error.message || 'Error al analizar los archivos');
    } finally {
      onLoadingChange(false);
    }
  };

  const handleFileSelect = (event) => {
    handleFiles(event.target.files);
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  return (
    <div className="file-upload">
      <div className="file-upload__form">
        <div className="file-upload__prompt">
          <label htmlFor="custom-prompt">Prompt personalizado (opcional):</label>
          <textarea
            id="custom-prompt"
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            placeholder="Ej: Analiza especialmente los balances de caja y detecta errores de suma..."
            rows={3}
            disabled={loading}
          />
        </div>
        
        <div 
          className={`file-upload__area ${dragActive ? 'file-upload__area--active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="file-upload__icon">📁</div>
          <p className="file-upload__text">
            Arrastra archivos Excel aquí o haz clic para seleccionar
          </p>
          <p className="file-upload__subtext">
            Formatos soportados: .xlsx, .xls (máximo 10MB por archivo)
          </p>
          
          <input
            ref={fileInputRef}
            type="file"
            accept=".xlsx,.xls"
            multiple
            onChange={handleFileSelect}
            style={{ display: 'none' }}
            disabled={loading}
          />
          
          <button
            type="button"
            onClick={handleButtonClick}
            disabled={loading}
            className="file-upload__button"
          >
            {loading ? 'Analizando...' : 'Seleccionar Archivos'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default FileUpload; 