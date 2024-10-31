// src/components/Login.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { FaUser, FaEye, FaEyeSlash } from 'react-icons/fa';
import Logo from './Logo';
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', { email, password });
      setMessage(response.data.message);

      // Armazena o indicador de autenticação
      localStorage.setItem('isAuthenticated', 'true');
      navigate('/'); // Redireciona para a página inicial
    } catch (error) {
      setMessage(error.response?.data?.error || 'Erro ao fazer login');
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <Logo /> {/* Logotipo adicionada aqui */}
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <div className="input-container">
            <FaUser className="input-icon" />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-container">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <div className="toggle-password" onClick={() => setShowPassword(!showPassword)}>
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </div>
          </div>
          <button className="form-button">Entrar</button>
        </form>
        {message && <p>{message}</p>}
        <p>Não tem uma conta? <Link to="/register" className="form-link">Registre-se aqui</Link></p>
      </div>
      <div className="login-image" />
    </div>
  );
}

export default Login;
