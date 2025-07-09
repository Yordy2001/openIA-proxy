import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResultsDisplay from './components/ResultsDisplay';
import ChatComponent from './components/ChatComponent';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showChat, setShowChat] = useState(false);

  const handleAnalysisComplete = (analysisResults) => {
    setResults(analysisResults);
    setError(null);
  };

  const handleAnalysisError = (errorMessage) => {
    setError(errorMessage);
    setResults(null);
  };

  const handleLoadingChange = (isLoading) => {
    setLoading(isLoading);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧾 Análisis Contable con IA</h1>
        <p>Sube archivos Excel para análisis automático</p>
      </header>
      
      <main className="App-main">
        <FileUpload 
          onAnalysisComplete={handleAnalysisComplete}
          onAnalysisError={handleAnalysisError}
          onLoadingChange={handleLoadingChange}
          loading={loading}
        />
        
        {error && (
          <div className="error-message">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}
        
        {results && (
          <ResultsDisplay 
            results={results}
            onChatToggle={() => setShowChat(!showChat)}
            showChat={showChat}
          />
        )}
        
        {showChat && results?.session_id && (
          <ChatComponent 
            sessionId={results.session_id}
            onClose={() => setShowChat(false)}
          />
        )}
      </main>
    </div>
  );
}

export default App; 