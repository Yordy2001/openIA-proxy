import axios from 'axios';

// Configuration
const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:7000',
  timeout: 60000, // 60 seconds for large files
};

// Create axios instance
const apiClient = axios.create(API_CONFIG);

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error);
    
    // Extract meaningful error message
    if (error.response) {
      const errorData = error.response.data;
      const message = errorData.detail || errorData.error || 'Error del servidor';
      throw new Error(message);
    } else if (error.request) {
      throw new Error('No se pudo conectar con el servidor. Verifica que esté funcionando.');
    } else {
      throw new Error('Error al enviar la petición');
    }
  }
);

// API Service class
class ApiService {
  // Health Check
  async healthCheck() {
    const response = await apiClient.get('/health');
    return response.data;
  }

  // Server Info
  async getServerInfo() {
    const response = await apiClient.get('/');
    return response.data;
  }

  // Analysis
  async analyzeFiles(files, prompt = '') {
    const formData = new FormData();
    
    // Add files to FormData
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }
    
    // Add prompt if exists
    if (prompt.trim()) {
      formData.append('prompt', prompt);
    }

    const response = await apiClient.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        console.log(`📤 Upload Progress: ${percentCompleted}%`);
      },
    });

    return response.data;
  }

  // Chat
  async sendChatMessage(sessionId, message) {
    const response = await apiClient.post('/chat', {
      session_id: sessionId,
      message: message
    });
    return response.data;
  }

  // Sessions
  async getSessions() {
    const response = await apiClient.get('/sessions');
    return response.data;
  }

  async getSessionDetails(sessionId) {
    const response = await apiClient.get(`/sessions/${sessionId}`);
    return response.data;
  }

  async deleteSession(sessionId) {
    const response = await apiClient.delete(`/sessions/${sessionId}`);
    return response.data;
  }

  // Excel Operations
  async extractExcelData(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post('/extract', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  async editCell(sheetName, row, column, value) {
    const response = await apiClient.post('/edit', {
      sheet_name: sheetName,
      row: row,
      column: column,
      value: value
    });
    return response.data;
  }

  async downloadExcel(filename, sheets) {
    const response = await apiClient.post('/download', {
      filename: filename,
      sheets: sheets
    }, {
      responseType: 'blob'
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);

    return true;
  }
}

// Export singleton instance
export default new ApiService(); 