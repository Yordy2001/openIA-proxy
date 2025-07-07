import React from 'react';

const ResultsDisplay = ({ results, error }) => {
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
      <h2>Resultados del Análisis</h2>
      
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

      {/* Metadata */}
      {results.metadata && Object.keys(results.metadata).length > 0 && (
        <div style={{ marginBottom: '30px' }}>
          <h3>📈 Información Adicional</h3>
          <div style={{ padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
            {Object.entries(results.metadata).map(([key, value]) => (
              <div key={key} style={{ marginBottom: '5px' }}>
                <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value) : value}
              </div>
            ))}
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