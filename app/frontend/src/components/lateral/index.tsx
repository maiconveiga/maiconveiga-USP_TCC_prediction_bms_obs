// import { useState } from 'react';
// import './style.css';

// interface LateralProps {
//   setForecastChiller: React.Dispatch<React.SetStateAction<any[]>>;
//   setTrainResult: React.Dispatch<React.SetStateAction<any[]>>; // Novo estado para os resultados do treino
// }

// const Lateral: React.FC<LateralProps> = ({ setForecastChiller, setTrainResult }) => {
//   const [isExpanded, setIsExpanded] = useState(false);
//   const [chiller, setChiller] = useState('');
//   const [valor, setValor] = useState('');
//   const [siteID, setSiteID] = useState(0); // Campo siteID (número)
//   const [siteName, setSiteName] = useState(''); // Campo siteName (string)
//   const [isLoading, setIsLoading] = useState(false);
//   const [isTraining, setIsTraining] = useState(false); // Controle do botão "Treinar"

//   const handleMouseEnter = () => setIsExpanded(true);
//   const handleMouseLeave = () => setIsExpanded(false);

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setIsLoading(true);

//     const data = {
//       ur_temp_saida: parseFloat(valor),
//       chiller: parseInt(chiller, 10),
//     };

//     try {
//       const response = await fetch('http://localhost:9001/forecast/chiller', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//       });

//       if (!response.ok) {
//         throw new Error('Erro na solicitação');
//       }

//       const result = await response.json();
//       setForecastChiller(result);
//     } catch (error) {
//       console.error('Erro ao enviar a solicitação:', error);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleTrain = async () => {
//     setIsTraining(true);

//     const trainData = {
//       siteID,
//       siteName,
//     };

//     try {
//       const response = await fetch('http://localhost:9001/train', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(trainData),
//       });

//       if (!response.ok) {
//         throw new Error('Erro ao treinar os modelos');
//       }

//       const result = await response.json();
//       setTrainResult(result); // Define os resultados do treinamento
//     } catch (error) {
//       console.error('Erro ao treinar:', error);
//     } finally {
//       setIsTraining(false);
//     }
//   };

//   return (
//     <aside
//       className={`sidebar ${isExpanded ? 'expanded' : ''}`}
//       onMouseEnter={handleMouseEnter}
//       onMouseLeave={handleMouseLeave}
//     >
//       <button className="menu-button" onClick={() => setIsExpanded(!isExpanded)}>
//         ☰
//       </button>
//       {isExpanded && (
//         <div className="menu-content">
//           <h1>Parâmetros de entrada</h1>
//           <form onSubmit={handleSubmit} method="post">
//             <div className="form-group">
//               <label htmlFor="chiller">Selecionar Chiller:</label>
//               <select
//                 id="chiller"
//                 name="chiller"
//                 value={chiller}
//                 onChange={(e) => setChiller(e.target.value)}
//                 required
//               >
//                 <option value="" disabled>
//                   Escolha uma opção
//                 </option>
//                 <option value="1">Chiller 1</option>
//                 <option value="2">Chiller 2</option>
//               </select>
//             </div>

//             <div className="form-group">
//               <label htmlFor="valor">Setpoint chiller (°C):</label>
//               <input
//                 type="number"
//                 id="valor"
//                 name="valor"
//                 step="0.5"
//                 placeholder="Defina o setpoint"
//                 value={valor}
//                 onChange={(e) => setValor(e.target.value)}
//                 min="4"
//                 max="12"
//                 required
//               />
//             </div>

//             <button type="submit" disabled={isLoading}>
//               {isLoading ? 'Enviando...' : 'Enviar'}
//             </button>
//           </form>

//           {/* Campos siteID e siteName */}
//           <div className="form-group">
//             <label htmlFor="siteID">Site ID:</label>
//             <input
//               type="number"
//               id="siteID"
//               name="siteID"
//               placeholder="Digite o Site ID"
//               value={siteID}
//               onChange={(e) => setSiteID(Number(e.target.value))}
//               required
//             />
//           </div>
//           <div className="form-group">
//             <label htmlFor="siteName">Site Name:</label>
//             <input
//               type="text"
//               id="siteName"
//               name="siteName"
//               placeholder="Digite o nome do site"
//               value={siteName}
//               onChange={(e) => setSiteName(e.target.value)}
//               required
//             />
//           </div>

//           {/* Botão Treinar */}
//           <button className="train-button" onClick={handleTrain} disabled={isTraining}>
//             {isTraining ? 'Treinando...' : 'Treinar'}
//           </button>
//         </div>
//       )}
//     </aside>
//   );
// };

// export default Lateral;

import { useState } from 'react';
import './style.css';

interface LateralProps {
  setForecastChiller: React.Dispatch<React.SetStateAction<any[]>>;
  setTrainResult: React.Dispatch<React.SetStateAction<any[]>>;
}

const Lateral: React.FC<LateralProps> = ({ setForecastChiller, setTrainResult }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [chiller, setChiller] = useState('');
  const [valor, setValor] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTraining, setIsTraining] = useState(false); // Controle do botão "Treinar"
  const [siteID, setSiteID] = useState(0);
  const [siteName, setSiteName] = useState('');

  const handleMouseEnter = () => setIsExpanded(true);
  const handleMouseLeave = () => setIsExpanded(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    const data = {
      ur_temp_saida: parseFloat(valor),
      chiller: parseInt(chiller, 10),
    };

    try {
      const response = await fetch('http://localhost:9001/forecast/chiller', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Erro na solicitação');
      }

      const result = await response.json();
      setForecastChiller(result);
    } catch (error) {
      console.error('Erro ao enviar a solicitação:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTrain = async () => {
    setIsTraining(true); // Desabilita o botão no início do POST
    setTrainResult([]); // Limpa os resultados anteriores
  
    const data = {
      siteID: parseInt(siteID, 10), // Valores do novo campo
      siteName,
    };
  
    try {
      const response = await fetch('http://localhost:9001/train', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error('Erro ao treinar os modelos');
      }
  
      const result = await response.json();
      setTrainResult(result); // Define os resultados do treinamento
    } catch (error) {
      console.error('Erro ao treinar:', error);
    } finally {
      setIsTraining(false); // Libera o botão somente após o POST retornar
    }
  };
  
  return (
    <aside
      className={`sidebar ${isExpanded ? 'expanded' : ''}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <button className="menu-button" onClick={() => setIsExpanded(!isExpanded)}>
        ☰
      </button>
      {isExpanded && (
        <div className="menu-content">
          <h1>Parâmetros de entrada</h1>
          <form onSubmit={handleSubmit} method="post">
            <div className="form-group">
              <label htmlFor="chiller">Selecionar Chiller:</label>
              <select
                id="chiller"
                name="chiller"
                value={chiller}
                onChange={(e) => setChiller(e.target.value)}
                required
              >
                <option value="" disabled>
                  Escolha uma opção
                </option>
                <option value="1">Chiller 1</option>
                <option value="2">Chiller 2</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="valor">Setpoint chiller (°C):</label>
              <input
                type="number"
                id="valor"
                name="valor"
                step="0.5"
                placeholder="Defina o setpoint"
                value={valor}
                onChange={(e) => setValor(e.target.value)}
                min="4"
                max="12"
                required
              />
            </div>

            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Enviando...' : 'Enviar'}
            </button>
          </form>

          {/* Campos adicionais para o botão "Treinar" */}
          {/* <div className="form-group">
            <label htmlFor="siteID">Site ID:</label>
            <input
              type="number"
              id="siteID"
              name="siteID"
              placeholder="Digite o ID do site"
              value={siteID}
              onChange={(e) => setSiteID(Number(e.target.value))}
              required
            />
          </div> */}

          {/* <div className="form-group">
            <label htmlFor="siteName">Site Name:</label>
            <input
              type="text"
              id="siteName"
              name="siteName"
              placeholder="Digite o nome do site"
              value={siteName}
              onChange={(e) => setSiteName(e.target.value)}
              required
            />
          </div> */}

          {/* <button className="train-button" onClick={handleTrain} disabled={isTraining}>
            {isTraining ? 'Treinando...' : 'Treinar'}
          </button> */}
        </div>
      )}
    </aside>
  );
};

export default Lateral;
