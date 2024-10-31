import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';
import Logo from './Logo';


function Home() {
  const navigate = useNavigate();
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([
    { id: 1, title: "Chat 1", lastModified: new Date().toLocaleString() },
    { id: 2, title: "Chat 2", lastModified: new Date().toLocaleString() }
  ]);

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    navigate('/login');
  };

  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');

    try {
      const response = await fetch('http://localhost:5000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input })
      });
      const data = await response.json();
      const botMessage = { sender: 'bot', text: data.response };

      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Erro ao se comunicar com o servidor:", error);
      setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: 'Erro ao se comunicar com o servidor.' }]);
    }
  };

  const handleNewChat = () => {
    const newChat = { id: Date.now(), title: `Chat ${conversations.length + 1}`, lastModified: new Date().toLocaleString() };
    setConversations((prevConversations) => [...prevConversations, newChat]);
    setMessages([{ sender: 'bot', text: 'Olá! Como posso ajudar?' }]);
  };

  const handleDeleteChat = (id) => {
    setConversations(conversations.filter(chat => chat.id !== id));
  };

  return (
    <div className="container">
      <div className="sidebar">
        <Logo/>
        <h3>Conversations</h3>
        <button className="new-chat-btn" onClick={handleNewChat}>+ Novo Chat</button>
        <ul>
          {conversations.map((conv) => (
            <li key={conv.id} className="conversation-item">
              <div className="chat-info">
                <span>{conv.title}</span>
                <small className="chat-date">{conv.lastModified}</small>
              </div>
              <i className="fas fa-trash delete-icon" onClick={() => handleDeleteChat(conv.id)}></i>
            </li>
          ))}
        </ul>

        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      </div>

      <div className="chat-section">
        <h2>Chatbot</h2>
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Digite sua mensagem..."
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <button onClick={handleSend}>Enviar</button>
        </div>
      </div>
    </div>
  );
}

export default Home;
