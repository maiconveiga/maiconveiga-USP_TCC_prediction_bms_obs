import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  
  build: {
    // Diretório de saída do build
    outDir: 'dist',
    // Diretório para os ativos (CSS, JS, etc.)
    assetsDir: 'assets',
    // Garante que o diretório de saída é limpo antes de cada build
    emptyOutDir: true,
  },
  server: {
    
    host: '0.0.0.0',  // Permite que o servidor seja acessível externamente
    port: 3000,        // Porta padrão do Vite, ajuste se necessário
  }
});
