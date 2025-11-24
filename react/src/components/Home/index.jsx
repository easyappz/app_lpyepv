import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMessages, sendMessage } from '../../api/messages';
import './Home.css';

export const Home = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUsername = localStorage.getItem('username');

    if (!token) {
      navigate('/login');
      return;
    }

    if (storedUsername) {
      setUsername(storedUsername);
    }

    loadMessages(token);
  }, [navigate]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadMessages = async (token) => {
    try {
      setLoading(true);
      const data = await getMessages(token, 100, 0);
      setMessages(data.messages || []);
    } catch (error) {
      console.error('Ошибка загрузки сообщений:', error);
      if (error.response?.status === 401) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!newMessage.trim() || sending) {
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      setSending(true);
      await sendMessage(token, newMessage.trim());
      setNewMessage('');
      await loadMessages(token);
    } catch (error) {
      console.error('Ошибка отправки сообщения:', error);
      if (error.response?.status === 401) {
        handleLogout();
      }
    } finally {
      setSending(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  return (
    <div className="home-container" data-easytag="id1-react/src/components/Home/index.jsx">
      <div className="chat-header">
        <div className="header-content">
          <h1 className="chat-title">Групповой чат</h1>
          <div className="user-info">
            <span className="username-display">{username}</span>
            <button className="logout-button" onClick={handleLogout}>
              Выйти
            </button>
          </div>
        </div>
      </div>

      <div className="messages-container">
        {loading ? (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Загрузка сообщений...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="empty-state">
            <p>Пока нет сообщений. Будьте первым!</p>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message-item ${message.username === username ? 'own-message' : 'other-message'}`}
              >
                <div className="message-header">
                  <span className="message-username">{message.username}</span>
                  <span className="message-time">{formatTime(message.created_at)}</span>
                </div>
                <div className="message-text">{message.text}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="message-input-container">
        <form onSubmit={handleSendMessage} className="message-form">
          <input
            type="text"
            className="message-input"
            placeholder="Введите сообщение..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            maxLength={1000}
            disabled={sending}
          />
          <button
            type="submit"
            className="send-button"
            disabled={!newMessage.trim() || sending}
          >
            {sending ? 'Отправка...' : 'Отправить'}
          </button>
        </form>
      </div>
    </div>
  );
};
