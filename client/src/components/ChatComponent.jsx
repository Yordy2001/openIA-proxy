import React, { useState, useRef, useEffect } from 'react';
import apiService from '../services/api';

const ChatComponent = ({ sessionId, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiService.sendChatMessage(sessionId, inputMessage.trim());
      
      const assistantMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      setError(error.message || 'Error al enviar el mensaje');
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="chat-component">
      <div className="chat-component__header">
        <h3>💬 Chat con IA</h3>
        <button 
          onClick={onClose}
          className="chat-component__close"
          aria-label="Cerrar chat"
        >
          ❌
        </button>
      </div>

      <div className="chat-component__messages">
        {messages.length === 0 && (
          <div className="chat-component__welcome">
            <p>¡Hola! Soy tu asistente de análisis contable. Puedes preguntarme sobre los resultados del análisis.</p>
            <div className="chat-component__suggestions">
              <p>Ejemplos de preguntas:</p>
              <ul>
                <li>¿Cuáles son los errores más críticos?</li>
                <li>¿Cómo puedo corregir el desbalance en la hoja X?</li>
                <li>¿Qué recomendaciones debo priorizar?</li>
              </ul>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${message.role === 'user' ? 'chat-message--user' : 'chat-message--assistant'}`}
          >
            <div className="chat-message__content">
              <p>{message.content}</p>
            </div>
            <div className="chat-message__timestamp">
              {formatTime(message.timestamp)}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="chat-message chat-message--assistant">
            <div className="chat-message__content">
              <div className="chat-message__loading">
                <span>🤔</span>
                <span>Pensando...</span>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="chat-message chat-message--error">
            <div className="chat-message__content">
              <p>❌ Error: {error}</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="chat-component__form">
        <div className="chat-component__input-group">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Escribe tu pregunta sobre el análisis..."
            disabled={isLoading}
            className="chat-component__input"
          />
          <button
            type="submit"
            disabled={isLoading || !inputMessage.trim()}
            className="chat-component__send-button"
          >
            {isLoading ? '⏳' : '➤'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatComponent; 