// src/apm.js
import { init as initApm } from '@elastic/apm-rum';

const apm = initApm({
  serviceName: 'frontend-next-js',
  serverUrl: 'http://localhost:8200',
  distributedTracingOrigins: ['http://localhost:9001'],
});

export default apm;
