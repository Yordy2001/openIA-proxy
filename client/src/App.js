import React, { useState, useEffect } from 'react';
import FileUpload from './FileUpload';
import ResultsDisplay from './ResultsDisplay';
import ExcelExtractor from './ExcelExtractor';
import apiService from './apiService';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [serverStatus, setServerStatus] = useState(null);
  const [activeTab, setActiveTab] = useState('analysis');

  useEffect(() => {
    checkServerStatus();
  }, []);

  const checkServerStatus = async () => {
    try {
      const status = await apiService.healthCheck();
      setServerStatus(status);
    } catch (error) {
      console.error('Error checking server status:', error);
      setServerStatus({
        status: 'error',
        message: 'No se pudo conectar con el servidor'
      });
    }
  };

  const handleAnalyze = async (files, prompt) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const analysisResults = await apiService.analyzeFiles(files, prompt);
      setResults(analysisResults);
    } catch (err) {
      setError(err.message || 'Error al analizar los archivos');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>📊 Análisis Contable con IA</h1>
          <p>Sube archivos Excel para detectar errores en cuadres contables</p>
          
          {/* Estado del servidor */}
          {serverStatus && (
            <div className={`server-status ${serverStatus.status}`}>
              <span>
                {serverStatus.status === 'healthy' ? '✅' : '❌'} 
                Servidor: {serverStatus.status === 'healthy' ? 'Conectado' : 'Desconectado'}
              </span>
              {serverStatus.ai_provider && (
                <span style={{ marginLeft: '10px' }}>
                  🤖 Proveedor: {serverStatus.ai_provider}
                </span>
              )}
            </div>
          )}
        </header>

        {/* Navegación por pestañas */}
        <div className="tabs">
          <button
            className={`tab-button ${activeTab === 'analysis' ? 'active' : ''}`}
            onClick={() => setActiveTab('analysis')}
          >
            🤖 Análisis IA
          </button>
          <button
            className={`tab-button ${activeTab === 'extractor' ? 'active' : ''}`}
            onClick={() => setActiveTab('extractor')}
          >
            📊 Tabla Editable
          </button>
        </div>

        {/* Contenido de las pestañas */}
        <div className="tab-content">
          {activeTab === 'analysis' && (
            <div className="tab-pane">
              {/* Componente de carga de archivos */}
              <FileUpload onAnalyze={handleAnalyze} isLoading={isLoading} />

              {/* Indicador de carga */}
              {isLoading && (
                <div className="loading">
                  <div className="spinner"></div>
                  <p>Analizando archivos... Esto puede tomar unos minutos.</p>
                </div>
              )}

              {/* Resultados o errores */}
              {(results || error) && (
                <div>
                  <div style={{ marginBottom: '20px', textAlign: 'center' }}>
                    <button onClick={handleReset} className="button">
                      🔄 Nuevo Análisis
                    </button>
                  </div>
                  <ResultsDisplay results={results} error={error} />
                </div>
              )}
            </div>
          )}

          {activeTab === 'extractor' && (
            <div className="tab-pane">
              <ExcelExtractor />
            </div>
          )}
        </div>

        {/* Footer */}
        <footer style={{ marginTop: '40px', textAlign: 'center', color: '#666' }}>
          <p>Desarrollado para análisis contable automatizado</p>
        </footer>
      </div>
    </div>
  );
}

export default App; 