import React from 'react';

const ResultsDisplay = ({ results, onChatToggle, showChat }) => {
  if (!results) return null;

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
      case 'alta':
        return '🚨';
      case 'medium':
      case 'media':
        return '⚠️';
      case 'low':
      case 'baja':
        return '💡';
      default:
        return '📝';
    }
  };

  const getSeverityClass = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
      case 'alta':
        return 'severity-high';
      case 'medium':
      case 'media':
        return 'severity-medium';
      case 'low':
      case 'baja':
        return 'severity-low';
      default:
        return 'severity-default';
    }
  };

  return (
    <div className="results-display">
      <div className="results-display__header">
        <h2>📊 Resultados del Análisis</h2>
        {results.session_id && (
          <button 
            onClick={onChatToggle}
            className={`results-display__chat-button ${showChat ? 'active' : ''}`}
          >
            💬 Chat IA
          </button>
        )}
      </div>

      {results.metadata?.analysis_date && (
        <div className="results-display__metadata">
          <p><strong>Fecha del análisis:</strong> {formatDate(results.metadata.analysis_date)}</p>
          {results.metadata.files_analyzed && (
            <p><strong>Archivos analizados:</strong> {results.metadata.files_analyzed.join(', ')}</p>
          )}
        </div>
      )}

      <div className="results-display__summary">
        <h3>📋 Resumen Ejecutivo</h3>
        <p>{results.summary}</p>
      </div>

      {results.findings && results.findings.length > 0 && (
        <div className="results-display__findings">
          <h3>🔍 Hallazgos Detallados</h3>
          <div className="findings-list">
            {results.findings.map((finding, index) => (
              <div key={index} className={`finding-item ${getSeverityClass(finding.severity)}`}>
                <div className="finding-header">
                  <span className="finding-icon">{getSeverityIcon(finding.severity)}</span>
                  <span className="finding-severity">{finding.severity || 'Normal'}</span>
                  {finding.sheet && (
                    <span className="finding-location">
                      📄 {finding.sheet}
                      {finding.row && ` (Fila ${finding.row})`}
                    </span>
                  )}
                </div>
                <p className="finding-description">{finding.description}</p>
                {finding.amount && (
                  <p className="finding-amount">
                    <strong>Monto:</strong> ${finding.amount.toLocaleString()}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {results.recommendations && results.recommendations.length > 0 && (
        <div className="results-display__recommendations">
          <h3>💡 Recomendaciones</h3>
          <div className="recommendations-list">
            {results.recommendations.map((rec, index) => (
              <div key={index} className="recommendation-item">
                <div className="recommendation-header">
                  <span className="recommendation-icon">
                    {rec.priority === 'high' ? '🔴' : rec.priority === 'medium' ? '🟡' : '🟢'}
                  </span>
                  <span className="recommendation-priority">
                    {rec.priority === 'high' ? 'Alta' : rec.priority === 'medium' ? 'Media' : 'Baja'}
                  </span>
                </div>
                <p className="recommendation-description">{rec.description}</p>
                {rec.action && (
                  <p className="recommendation-action">
                    <strong>Acción sugerida:</strong> {rec.action}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {typeof results.recommendations === 'string' && (
        <div className="results-display__recommendations">
          <h3>💡 Recomendaciones</h3>
          <p>{results.recommendations}</p>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay; 