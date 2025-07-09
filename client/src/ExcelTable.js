import React, { useState, useEffect } from 'react';
import apiService from './apiService';

const ExcelTable = ({ structuredData, onDataChange }) => {
  const [editingCell, setEditingCell] = useState(null);
  const [tempValue, setTempValue] = useState('');
  const [activeSheet, setActiveSheet] = useState(0);
  const [isDownloading, setIsDownloading] = useState(false);

  useEffect(() => {
    // Reset active sheet when data changes
    setActiveSheet(0);
  }, [structuredData]);

  const handleCellDoubleClick = (sheetIndex, rowIndex, columnName) => {
    setEditingCell({ sheetIndex, rowIndex, columnName });
    setTempValue(structuredData.sheets[sheetIndex].rows[rowIndex][columnName] || '');
  };

  const handleCellChange = (event) => {
    setTempValue(event.target.value);
  };

  const handleCellSubmit = async () => {
    if (editingCell && onDataChange) {
      try {
        const { sheetIndex, rowIndex, columnName } = editingCell;
        const newValue = tempValue === '' ? null : tempValue;
        
        // Update local data
        const updatedData = { ...structuredData };
        updatedData.sheets[sheetIndex].rows[rowIndex][columnName] = newValue;
        
        // Call parent callback
        onDataChange(updatedData);
        
        // Reset editing state
        setEditingCell(null);
        setTempValue('');
      } catch (error) {
        console.error('Error updating cell:', error);
        alert('Error al actualizar la celda: ' + error.message);
      }
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleCellSubmit();
    } else if (event.key === 'Escape') {
      setEditingCell(null);
      setTempValue('');
    }
  };

  const handleDownload = async () => {
    setIsDownloading(true);
    try {
      await apiService.downloadExcel(structuredData.filename, structuredData.sheets);
      alert('Archivo descargado exitosamente');
    } catch (error) {
      console.error('Error downloading file:', error);
      alert('Error al descargar el archivo: ' + error.message);
    } finally {
      setIsDownloading(false);
    }
  };

  const renderCell = (value, sheetIndex, rowIndex, columnName, isNumeric) => {
    const isEditing = editingCell?.sheetIndex === sheetIndex && 
                     editingCell?.rowIndex === rowIndex && 
                     editingCell?.columnName === columnName;

    if (isEditing) {
      return (
        <input
          type="text"
          value={tempValue}
          onChange={handleCellChange}
          onKeyDown={handleKeyDown}
          onBlur={handleCellSubmit}
          style={{
            width: '100%',
            padding: '4px',
            border: '2px solid #007bff',
            borderRadius: '2px',
            fontSize: '14px'
          }}
          autoFocus
        />
      );
    }

    const displayValue = value === null || value === undefined ? '' : value;
    
    return (
      <div
        onClick={() => handleCellDoubleClick(sheetIndex, rowIndex, columnName)}
        style={{
          padding: '8px',
          cursor: 'pointer',
          minHeight: '20px',
          textAlign: isNumeric ? 'right' : 'left',
          backgroundColor: 'transparent',
          border: '1px solid transparent',
          borderRadius: '2px',
          transition: 'all 0.2s ease'
        }}
        onMouseEnter={(e) => {
          e.target.style.backgroundColor = '#f8f9fa';
          e.target.style.border = '1px solid #dee2e6';
        }}
        onMouseLeave={(e) => {
          e.target.style.backgroundColor = 'transparent';
          e.target.style.border = '1px solid transparent';
        }}
        title="Doble clic para editar"
      >
        {displayValue}
      </div>
    );
  };

  if (!structuredData || !structuredData.sheets || structuredData.sheets.length === 0) {
    return (
      <div className="excel-table">
        <h3>📊 Datos del Excel</h3>
        <p>No hay datos para mostrar</p>
      </div>
    );
  }

  const currentSheet = structuredData.sheets[activeSheet];

  return (
    <div className="excel-table">
      <div className="excel-header">
        <h3>📊 Datos del Excel: {structuredData.filename}</h3>
        <div className="excel-actions">
          <button
            onClick={handleDownload}
            disabled={isDownloading}
            className="button"
            style={{ backgroundColor: '#28a745', marginRight: '10px' }}
          >
            {isDownloading ? '⏳ Descargando...' : '📥 Descargar Excel'}
          </button>
        </div>
      </div>

      {/* Sheet Tabs */}
      {structuredData.sheets.length > 1 && (
        <div className="sheet-tabs">
          {structuredData.sheets.map((sheet, index) => (
            <button
              key={index}
              className={`sheet-tab ${index === activeSheet ? 'active' : ''}`}
              onClick={() => setActiveSheet(index)}
            >
              📄 {sheet.sheet_name}
            </button>
          ))}
        </div>
      )}

      {/* Sheet Info */}
      <div className="sheet-info">
        <h4>📋 Hoja: {currentSheet.sheet_name}</h4>
        <p>
          <strong>Dimensiones:</strong> {currentSheet.shape[0]} filas × {currentSheet.shape[1]} columnas
          {currentSheet.numeric_columns.length > 0 && (
            <span style={{ marginLeft: '20px' }}>
              <strong>Columnas numéricas:</strong> {currentSheet.numeric_columns.join(', ')}
            </span>
          )}
        </p>
      </div>

      {/* Table */}
      <div className="table-container">
        <table className="excel-data-table">
          <thead>
            <tr>
              <th style={{ width: '50px', textAlign: 'center' }}>#</th>
              {currentSheet.columns.map((column, index) => (
                <th key={index} style={{ minWidth: '120px' }}>
                  {column}
                  {currentSheet.numeric_columns.includes(column) && (
                    <span style={{ marginLeft: '5px', fontSize: '12px' }}>🔢</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {currentSheet.rows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                <td style={{ textAlign: 'center', backgroundColor: '#f8f9fa', fontWeight: 'bold' }}>
                  {rowIndex + 1}
                </td>
                {currentSheet.columns.map((column, colIndex) => (
                  <td key={colIndex} style={{ padding: '0' }}>
                    {renderCell(
                      row[column],
                      activeSheet,
                      rowIndex,
                      column,
                      currentSheet.numeric_columns.includes(column)
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Instructions */}
      <div className="table-instructions">
        <p><strong>💡 Instrucciones:</strong></p>
        <ul>
          <li>Haz doble clic en cualquier celda para editarla</li>
          <li>Presiona Enter para guardar cambios o Escape para cancelar</li>
          <li>Las columnas numéricas se muestran alineadas a la derecha</li>
          <li>Usa las pestañas para navegar entre hojas</li>
          <li>Haz clic en "Descargar Excel" para obtener el archivo modificado</li>
        </ul>
      </div>
    </div>
  );
};

export default ExcelTable; 