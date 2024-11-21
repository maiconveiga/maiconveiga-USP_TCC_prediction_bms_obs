// index.tsx ou index.js (dependendo de sua configuração)
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './style.css'; // Caso tenha um arquivo de estilo global
import apm from './apm'

console.log(apm);

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
