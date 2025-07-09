import React from 'react';
import { useState } from 'react';
import ChatComponent from './ChatComponent';

const ResultsDisplay = ({ results, error }) => {
  const [showChat, setShowChat] = useState(false);

  if (error) {
    return (
      <div className="results">
        <h2>Error en el Análisis</h2>
        <div style={{ color: 'red', padding: '20px', backgroundColor: '#ffebee', borderRadius: '4px' }}>
          {error}
        </div>
      </div>
    );
  }

  if (!results) {
    return null;
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'high':
        return '🔴';
      case 'medium':
        return '🟡';
      case 'low':
        return '🟢';
      default:
        return '⚪';
    }
  };

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return '🔴';
      case 'medium':
        return '🟡';
      case 'low':
        return '🟢';
      default:
        return '⚪';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'info':
        return 'ℹ️';
      default:
        return '📋';
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'calculation':
        return '🧮';
      case 'format':
        return '📋';
      case 'process':
        return '⚙️';
      case 'validation':
        return '✅';
      default:
        return '📌';
    }
  };

  return (
    <div className="results">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Resultados del Análisis</h2>
        {results.session_id && (
          <button 
            onClick={() => setShowChat(!showChat)}
            className="button"
            style={{ backgroundColor: '#28a745' }}
          >
            {showChat ? '🔒 Cerrar Chat' : '💬 Chat IA'}
          </button>
        )}
      </div>
      
      {/* Chat Component */}
      {showChat && results.session_id && (
        <ChatComponent 
          sessionId={results.session_id} 
          onClose={() => setShowChat(false)}
        />
      )}
      
      {/* Resumen */}
      <div style={{ marginBottom: '30px' }}>
        <h3>📊 Resumen</h3>
        <div style={{ padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
          {results.summary}
        </div>
      </div>

      {/* Hallazgos */}
      {results.findings && results.findings.length > 0 && (
        <div style={{ marginBottom: '30px' }}>
          <h3>🔍 Hallazgos ({results.findings.length})</h3>
          {results.findings.map((finding, index) => (
            <div key={index} className={`finding ${finding.type}`}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ marginRight: '10px' }}>
                  {getTypeIcon(finding.type)}
                </span>
                <h4 style={{ margin: 0, flex: 1 }}>{finding.title}</h4>
                <span className={`severity-${finding.severity}`}>
                  {getSeverityIcon(finding.severity)} {finding.severity.toUpperCase()}
                </span>
              </div>
              
              <p style={{ margin: '10px 0', color: '#666' }}>
                {finding.description}
              </p>
              
              {finding.location && (
                <div style={{ marginBottom: '10px' }}>
                  <strong>📍 Ubicación:</strong> {finding.location}
                  {finding.sheet && (
                    <span> (Hoja: {finding.sheet})</span>
                  )}
                  {finding.row && (
                    <span> (Fila: {finding.row})</span>
                  )}
                </div>
              )}
              
              {finding.suggested_fix && (
                <div style={{ marginTop: '10px', padding: '10px', backgroundColor: '#e8f5e8', borderRadius: '4px' }}>
                  <strong>💡 Solución sugerida:</strong> {finding.suggested_fix}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Recomendaciones */}
      {results.recommendations && results.recommendations.length > 0 && (
        <div style={{ marginBottom: '30px' }}>
          <h3>📋 Recomendaciones ({results.recommendations.length})</h3>
          {results.recommendations.map((recommendation, index) => (
            <div key={index} className="recommendation">
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ marginRight: '10px' }}>
                  {getCategoryIcon(recommendation.category)}
                </span>
                <h4 style={{ margin: 0, flex: 1 }}>{recommendation.title}</h4>
                <span className={`priority-${recommendation.priority}`}>
                  {getPriorityIcon(recommendation.priority)} {recommendation.priority.toUpperCase()}
                </span>
              </div>
              
              <p style={{ margin: '10px 0', color: '#666' }}>
                {recommendation.description}
              </p>
              
              <div style={{ fontSize: '0.9em', color: '#888' }}>
                <strong>Categoría:</strong> {recommendation.category}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Metadata con información específica */}
      {results.metadata && Object.keys(results.metadata).length > 0 && (
        <div style={{ marginBottom: '30px' }}>
          <h3>📈 Información Adicional</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
            
            {/* Estadísticas generales */}
            <div style={{ padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
              <h4 style={{ margin: '0 0 15px 0', color: '#495057' }}>📊 Estadísticas Generales</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div><strong>Total de hallazgos:</strong> {results.metadata.total_findings || 0}</div>
                <div><strong>Problemas críticos:</strong> {results.metadata.critical_issues || 0}</div>
                <div><strong>Hojas analizadas:</strong> {results.metadata.sheets_analyzed || 0}</div>
              </div>
            </div>

            {/* Bancas no rentables */}
            {results.metadata.non_profitable_bancas && results.metadata.non_profitable_bancas.length > 0 && (
              <div style={{ padding: '15px', backgroundColor: '#fff3cd', borderRadius: '4px', border: '1px solid #ffeaa7' }}>
                <h4 style={{ margin: '0 0 15px 0', color: '#856404' }}>⚠️ Bancas No Rentables</h4>
                <ul style={{ margin: 0, paddingLeft: '20px' }}>
                  {results.metadata.non_profitable_bancas.map((banca, index) => (
                    <li key={index} style={{ color: '#856404', fontWeight: 'bold' }}>{banca}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Posibles errores de configuración */}
            {results.metadata.possible_config_errors && results.metadata.possible_config_errors.length > 0 && (
              <div style={{ padding: '15px', backgroundColor: '#f8d7da', borderRadius: '4px', border: '1px solid #f5c6cb' }}>
                <h4 style={{ margin: '0 0 15px 0', color: '#721c24' }}>🔧 Posibles Errores de Configuración</h4>
                <ul style={{ margin: 0, paddingLeft: '20px' }}>
                  {results.metadata.possible_config_errors.map((hoja, index) => (
                    <li key={index} style={{ color: '#721c24', fontWeight: 'bold' }}>{hoja}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Información técnica */}
            <div style={{ padding: '15px', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
              <h4 style={{ margin: '0 0 15px 0', color: '#1565c0' }}>🔧 Información Técnica</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div><strong>Proveedor:</strong> {results.metadata.provider || 'No especificado'}</div>
                <div><strong>Modelo:</strong> {results.metadata.model || 'No especificado'}</div>
                {results.session_id && (
                  <div><strong>Session ID:</strong> <code style={{ fontSize: '0.8em' }}>{results.session_id}</code></div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Resumen estadístico */}
      {(results.findings || results.recommendations) && (
        <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
          <h3>📊 Resumen Estadístico</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
            {results.findings && (
              <div>
                <strong>Hallazgos por Tipo:</strong>
                <ul>
                  <li>Errores: {results.findings.filter(f => f.type === 'error').length}</li>
                  <li>Advertencias: {results.findings.filter(f => f.type === 'warning').length}</li>
                  <li>Información: {results.findings.filter(f => f.type === 'info').length}</li>
                </ul>
              </div>
            )}
            
            {results.findings && (
              <div>
                <strong>Severidad:</strong>
                <ul>
                  <li>Alta: {results.findings.filter(f => f.severity === 'high').length}</li>
                  <li>Media: {results.findings.filter(f => f.severity === 'medium').length}</li>
                  <li>Baja: {results.findings.filter(f => f.severity === 'low').length}</li>
                </ul>
              </div>
            )}
            
            {results.recommendations && (
              <div>
                <strong>Prioridad de Recomendaciones:</strong>
                <ul>
                  <li>Alta: {results.recommendations.filter(r => r.priority === 'high').length}</li>
                  <li>Media: {results.recommendations.filter(r => r.priority === 'medium').length}</li>
                  <li>Baja: {results.recommendations.filter(r => r.priority === 'low').length}</li>
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
