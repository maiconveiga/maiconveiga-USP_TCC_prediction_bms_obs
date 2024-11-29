// import { useState } from 'react';
// import Lateral from './components/lateral';
// import Conteudo from './components/conteudo';
// import './style.css';


// function App() {
//   const [forecastChiller, setForecastChiller] = useState<any[]>([]);

//   return (
//     <div className="container">
//       <Lateral setForecastChiller={setForecastChiller} />
//       <Conteudo forecastChiller={forecastChiller} />
//     </div>
//   );
// }

// export default App;

import { useState } from 'react';
import Lateral from './components/lateral';
import Conteudo from './components/conteudo';
import './style.css';

function App() {
  const [forecastChiller, setForecastChiller] = useState<any[]>([]);
  const [trainResult, setTrainResult] = useState<any[]>([]); // Novo estado

  return (
    <div className="container">
      <Lateral
        setForecastChiller={setForecastChiller}
        setTrainResult={setTrainResult} // Passa o estado para o Lateral
      />
      <Conteudo
        forecastChiller={forecastChiller}
        trainResult={trainResult} // Passa os resultados para o Conteudo
      />
    </div>
  );
}

export default App;
