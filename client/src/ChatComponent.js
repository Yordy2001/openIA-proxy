import React, { useState, useEffect, useRef } from 'react';
import apiService from './apiService';

const ChatComponent = ({ sessionId, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    // Add user message to chat
    const newUserMessage = {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response = await apiService.sendChatMessage(sessionId, userMessage);
      
      // Add AI response to chat
      const aiMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h3>💬 Chat sobre el Análisis</h3>
        <button onClick={onClose} className="close-button">✕</button>
      </div>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              <strong>{message.role === 'user' ? 'Tú' : 'Asistente IA'}:</strong>
              <p>{message.content}</p>
            </div>
            <div className="message-time">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <strong>Asistente IA:</strong>
              <p>Escribiendo...</p>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {error && (
        <div className="chat-error">
          Error: {error}
        </div>
      )}
      
      <form onSubmit={handleSendMessage} className="chat-input">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Pregunta sobre el análisis..."
          disabled={isLoading}
          className="chat-input-field"
        />
        <button 
          type="submit" 
          disabled={isLoading || !inputMessage.trim()}
          className="chat-send-button"
        >
          Enviar
        </button>
      </form>
    </div>
  );
};

export default ChatComponent;
