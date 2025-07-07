import React, { useState } from 'react';

const FileUpload = ({ onAnalyze, isLoading }) => {
  const [files, setFiles] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [dragOver, setDragOver] = useState(false);

  const handleFileChange = (event) => {
    const selectedFiles = event.target.files;
    if (selectedFiles && selectedFiles.length > 0) {
      setFiles(selectedFiles);
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
    
    const droppedFiles = event.dataTransfer.files;
    if (droppedFiles && droppedFiles.length > 0) {
      setFiles(droppedFiles);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (files && files.length > 0) {
      onAnalyze(files, prompt);
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

  const validateFiles = () => {
    if (!files || files.length === 0) return false;
    
    for (let i = 0; i < files.length; i++) {
      if (!isExcelFile(files[i])) {
        alert(`El archivo ${files[i].name} no es un archivo Excel válido.`);
        return false;
      }
    }
    return true;
  };

  const canSubmit = files && files.length > 0 && !isLoading;

  return (
    <div className="upload-section">
      <h2>Subir Archivos Excel</h2>
      <form onSubmit={handleSubmit}>
        <div 
          className={`file-input ${dragOver ? 'drag-over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            type="file"
            multiple
            accept=".xlsx,.xls"
            onChange={handleFileChange}
            disabled={isLoading}
          />
          <div style={{ marginTop: '10px', color: '#666' }}>
            {files && files.length > 0 ? (
              <div>
                <p>Archivos seleccionados:</p>
                <ul>
                  {Array.from(files).map((file, index) => (
                    <li key={index}>
                      {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p>Arrastra archivos Excel aquí o haz clic para seleccionarlos</p>
            )}
          </div>
        </div>

        <div style={{ marginTop: '20px' }}>
          <label htmlFor="prompt">Prompt personalizado (opcional):</label>
          <textarea
            id="prompt"
            className="textarea"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Escribe aquí cualquier instrucción específica para el análisis..."
            disabled={isLoading}
          />
        </div>

        <button
          type="submit"
          className="button"
          disabled={!canSubmit || !validateFiles()}
        >
          {isLoading ? 'Analizando...' : 'Analizar Archivos'}
        </button>
      </form>
    </div>
  );
};

export default FileUpload; 