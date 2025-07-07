import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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
  }
};

export default apiService; 