import React from 'react';
import ExcelTable from './ExcelTable';
import ExcelExtractor from './ExcelExtractor';

// Mock data for testing
const mockExcelData = {
  filename: "test-data.xlsx",
  sheets: [
    {
      sheet_name: "Resumen Bancas",
      columns: ["Banca", "Ventas", "Premios", "Retiros", "Comisiones", "Neto"],
      rows: [
        { "Banca": "CH01", "Ventas": 8505, "Premios": 1840, "Retiros": 0, "Comisiones": 1020.6, "Neto": 5644.4 },
        { "Banca": "CH02", "Ventas": 34080, "Premios": 30600, "Retiros": 0, "Comisiones": 4089.6, "Neto": -609.6 },
        { "Banca": "CH03", "Ventas": 100, "Premios": 0, "Retiros": 0, "Comisiones": 12.0, "Neto": 88.0 },
        { "Banca": "CH04", "Ventas": 3385, "Premios": 300, "Retiros": 0, "Comisiones": 406.2, "Neto": 2678.8 },
        { "Banca": "CH05", "Ventas": 11107, "Premios": 0, "Retiros": 0, "Comisiones": 1332.84, "Neto": 9774.16 }
      ],
      shape: [5, 6],
      numeric_columns: ["Ventas", "Premios", "Retiros", "Comisiones", "Neto"]
    },
    {
      sheet_name: "Balance General",
      columns: ["Concepto", "Monto", "Porcentaje"],
      rows: [
        { "Concepto": "Ventas Totales", "Monto": 101000, "Porcentaje": 100.0 },
        { "Concepto": "Premios Pagados", "Monto": 60000, "Porcentaje": 59.41 },
        { "Concepto": "Comisiones", "Monto": 12120, "Porcentaje": 12.0 },
        { "Concepto": "Neto Final", "Monto": 28880, "Porcentaje": 28.59 }
      ],
      shape: [4, 3],
      numeric_columns: ["Monto", "Porcentaje"]
    },
    {
      sheet_name: "Movimientos Diarios",
      columns: ["Fecha", "Ventas_Dia", "Premios_Dia", "Comisiones_Dia", "Neto_Dia", "Observaciones"],
      rows: [
        { "Fecha": "2024-06-17", "Ventas_Dia": 12500, "Premios_Dia": 8200, "Comisiones_Dia": 1500, "Neto_Dia": 2800, "Observaciones": "Normal" },
        { "Fecha": "2024-06-18", "Ventas_Dia": 15800, "Premios_Dia": 9500, "Comisiones_Dia": 1896, "Neto_Dia": 4404, "Observaciones": "Alto" },
        { "Fecha": "2024-06-19", "Ventas_Dia": 14200, "Premios_Dia": 7800, "Comisiones_Dia": 1704, "Neto_Dia": 4696, "Observaciones": "Normal" },
        { "Fecha": "2024-06-20", "Ventas_Dia": 13600, "Premios_Dia": 8900, "Comisiones_Dia": 1632, "Neto_Dia": 3068, "Observaciones": "Normal" },
        { "Fecha": "2024-06-21", "Ventas_Dia": 16900, "Premios_Dia": 10200, "Comisiones_Dia": 2028, "Neto_Dia": 4672, "Observaciones": "Alto" }
      ],
      shape: [5, 6],
      numeric_columns: ["Ventas_Dia", "Premios_Dia", "Comisiones_Dia", "Neto_Dia"]
    }
  ],
  metadata: {
    "total_sheets": 3,
    "processed_at": "2025-07-08T16:10:38.398353",
    "data_key": "test-data.xlsx_12345"
  }
};

const TestComponents = () => {
  const [testData, setTestData] = React.useState(mockExcelData);
  const [showTable, setShowTable] = React.useState(false);

  const handleDataChange = (newData) => {
    setTestData(newData);
    console.log('Data changed:', newData);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>🧪 Prueba de Componentes</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <button
          onClick={() => setShowTable(!showTable)}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginRight: '10px'
          }}
        >
          {showTable ? 'Ocultar Tabla' : 'Mostrar Tabla de Prueba'}
        </button>
        
        <button
          onClick={() => setTestData(mockExcelData)}
          style={{
            padding: '10px 20px',
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Resetear Datos
        </button>
      </div>

      {showTable && (
        <div>
          <h2>📊 Tabla Excel (con datos mock)</h2>
          <ExcelTable
            structuredData={testData}
            onDataChange={handleDataChange}
          />
        </div>
      )}

      <div style={{ marginTop: '40px' }}>
        <h2>📁 Extractor de Excel</h2>
        <ExcelExtractor />
      </div>

      <div style={{ marginTop: '40px', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
        <h3>ℹ️ Información de Prueba</h3>
        <ul style={{ textAlign: 'left' }}>
          <li>✅ La tabla muestra datos mock con 3 hojas</li>
          <li>✅ Puedes hacer doble clic en las celdas para editarlas</li>
          <li>✅ Las pestañas funcionan para cambiar entre hojas</li>
          <li>✅ Las columnas numéricas se muestran alineadas a la derecha</li>
          <li>⚠️ La descarga necesita el servidor backend funcionando</li>
          <li>⚠️ La extracción de archivos necesita el servidor backend funcionando</li>
        </ul>
      </div>
    </div>
  );
};

export default TestComponents; 