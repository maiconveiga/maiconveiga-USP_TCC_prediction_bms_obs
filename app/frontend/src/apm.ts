import { init as initApm } from '@elastic/apm-rum';

const apm = initApm({
  serviceName: 'react-vite-app', // Nome do serviço (visível no Elastic APM)
  serverUrl: 'http://localhost:8200', // URL do APM Server
  serviceVersion: '1.0.0', // Versão do serviço (opcional)
  environment: import.meta.env.MODE, // Ambiente atual (desenvolvimento/produção)
});

export default apm;
