import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:7000';
console.log(process.env.REACT_APP_API_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 segundos para archivos grandes
});

export const apiService = {
  /**
   * Verificar el estado del servidor
   */
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },

  /**
   * Analizar archivos Excel
   * @param {FileList} files - Archivos Excel a analizar
   * @param {string} prompt - Prompt opcional para el análisis
   */
  async analyzeFiles(files, prompt = '') {
    try {
      const formData = new FormData();
      
      // Agregar archivos al FormData
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }
      
      // Agregar prompt si existe
      if (prompt.trim()) {
        formData.append('prompt', prompt);
      }

      const response = await api.post('/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          console.log(`Upload Progress: ${percentCompleted}%`);
        },
      });

      return response.data;
    } catch (error) {
      console.error('Error analyzing files:', error);
      
      // Extraer mensaje de error más específico
      if (error.response) {
        // El servidor respondió con un error
        const errorData = error.response.data;
        throw new Error(errorData.detail || errorData.error || 'Error del servidor');
      } else if (error.request) {
        // No hubo respuesta del servidor
        throw new Error('No se pudo conectar con el servidor. Verifica que esté funcionando.');
      } else {
        // Error en la configuración de la petición
        throw new Error('Error al enviar la petición');
      }
    }
  },

  /**
   * Obtener información básica del servidor
   */
  async getServerInfo() {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      console.error('Error getting server info:', error);
      throw error;
    }
  },

  /**
   * Enviar mensaje de chat basado en análisis previo
   * @param {string} sessionId - ID de la sesión del análisis
   * @param {string} message - Mensaje del usuario
   */
  async sendChatMessage(sessionId, message) {
    try {
      const response = await api.post('/chat', {
        session_id: sessionId,
        message: message
      });

      return response.data;
    } catch (error) {
      console.error('Error sending chat message:', error);
      
      if (error.response) {
        const errorData = error.response.data;
        throw new Error(errorData.detail || errorData.error || 'Error del servidor');
      } else if (error.request) {
        throw new Error('No se pudo conectar con el servidor');
      } else {
        throw new Error('Error al enviar el mensaje');
      }
    }
  },

  /**
   * Obtener lista de sesiones
   */
  async getSessions() {
    try {
      const response = await api.get('/sessions');
      return response.data;
    } catch (error) {
      console.error('Error getting sessions:', error);
      throw error;
    }
  },

  /**
   * Obtener detalles de una sesión específica
   * @param {string} sessionId - ID de la sesión
   */
  async getSessionDetails(sessionId) {
    try {
      const response = await api.get(`/sessions/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting session details:', error);
      throw error;
    }
  },

  /**
   * Eliminar una sesión
   * @param {string} sessionId - ID de la sesión a eliminar
   */
  async deleteSession(sessionId) {
    try {
      const response = await api.delete(`/sessions/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting session:', error);
      throw error;
    }
  },

  /**
   * Extraer datos estructurados de un archivo Excel
   * @param {File} file - Archivo Excel
   */
  async extractExcelData(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/extract', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      console.error('Error extracting Excel data:', error);
      
      if (error.response) {
        const errorData = error.response.data;
        throw new Error(errorData.detail || errorData.error || 'Error del servidor');
      } else if (error.request) {
        throw new Error('No se pudo conectar con el servidor');
      } else {
        throw new Error('Error al enviar la petición');
      }
    }
  },

  /**
   * Editar una celda específica
   * @param {string} sheetName - Nombre de la hoja
   * @param {number} row - Número de fila
   * @param {string} column - Nombre de columna
   * @param {any} value - Nuevo valor
   */
  async editCell(sheetName, row, column, value) {
    try {
      const response = await api.post('/edit', {
        sheet_name: sheetName,
        row: row,
        column: column,
        value: value
      });

      return response.data;
    } catch (error) {
      console.error('Error editing cell:', error);
      
      if (error.response) {
        const errorData = error.response.data;
        throw new Error(errorData.detail || errorData.error || 'Error del servidor');
      } else if (error.request) {
        throw new Error('No se pudo conectar con el servidor');
      } else {
        throw new Error('Error al enviar la petición');
      }
    }
  },

  /**
   * Descargar Excel modificado
   * @param {string} filename - Nombre del archivo
   * @param {Array} sheets - Datos de las hojas
   */
  async downloadExcel(filename, sheets) {
    try {
      const response = await api.post('/download', {
        filename: filename,
        sheets: sheets
      }, {
        responseType: 'blob'
      });

      // Crear URL para descarga
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      return { success: true, message: 'Archivo descargado exitosamente' };
    } catch (error) {
      console.error('Error downloading Excel:', error);
      
      if (error.response) {
        const errorData = error.response.data;
        throw new Error(errorData.detail || errorData.error || 'Error del servidor');
      } else if (error.request) {
        throw new Error('No se pudo conectar con el servidor');
      } else {
        throw new Error('Error al enviar la petición');
      }
    }
  }
};

export default apiService;
