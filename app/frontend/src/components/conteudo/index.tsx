// import './style.css';
// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
//   Legend,
//   ResponsiveContainer,
// } from 'recharts';

// interface ForecastData {
//   data_hora: string;
//   corrente: number;
//   vag: number;
//   ligados: number;
//   delta_ac: number;
//   tr: number;
//   kwh: number;
//   temperatura: number;
//   pressao: number;
//   torre: number;
//   umidade: number;
// }

// interface ConteudoProps {
//   forecastChiller: ForecastData[];
// }

// const Conteudo: React.FC<ConteudoProps> = ({ forecastChiller }) => {
//   const data = forecastChiller.map((item) => ({
//     dataHora: item.data_hora,
//     corrente: item.corrente,
//     vag: item.vag,
//     ligados: item.ligados,
//     delta_ac: item.delta_ac,
//     tr: item.tr,
//     kwh: item.kwh,
//     temperatura: item.temperatura,
//     pressao: item.pressao,
//     torre: item.torre,
//     umidade: item.umidade,
//   }));

//   const renderChart = (dataKey: keyof ForecastData, label: string, color: string) => (
//     <div className="chart-wrapper">
//       <h3>{label} ao Longo do Tempo</h3>
//       <ResponsiveContainer width="100%" height={400}>
//         <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 40 }}>
//           <CartesianGrid strokeDasharray="3 3" />
//           <XAxis
//             dataKey="dataHora"
//             tick={{ fontSize: 12 }}
//             angle={-45}
//             textAnchor="end"
//             height={70}
//           />
//           <YAxis
//             label={{ value: label, angle: -90, position: 'insideLeft', offset: 0 }}
//             tick={{ fontSize: 12 }}
//           />
//           <Tooltip formatter={(value: number) => `${value.toFixed(2)}`} />
//           <Legend verticalAlign="top" height={36} />
//           <Line type="monotone" dataKey={dataKey} stroke={color} activeDot={{ r: 8 }} name={label} />
//         </LineChart>
//       </ResponsiveContainer>
//     </div>
//   );

//   const renderCorrenteVagLigadosChart = () => (
//     <div className="chart-wrapper">
//       <h3>Análise de Corrente, VAG e Ligados ao Longo do Tempo</h3>
//       <ResponsiveContainer width="100%" height={400}>
//         <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 40 }}>
//           <CartesianGrid strokeDasharray="3 3" />
//           <XAxis
//             dataKey="dataHora"
//             tick={{ fontSize: 12 }}
//             angle={-45}
//             textAnchor="end"
//             height={70}
//           />
//           <YAxis
//             label={{ value: 'Valores (%)', angle: -90, position: 'insideLeft', offset: 0 }}
//             tick={{ fontSize: 12 }}
//           />
//           <Tooltip formatter={(value: number) => `${value.toFixed(2)}%`} />
//           <Legend verticalAlign="top" height={36} />
//           <Line type="monotone" dataKey="corrente" stroke="#8884d8" activeDot={{ r: 8 }} name="Corrente" />
//           <Line type="monotone" dataKey="vag" stroke="#82ca9d" activeDot={{ r: 8 }} name="VAG" />
//           <Line type="monotone" dataKey="ligados" stroke="#ff7300" activeDot={{ r: 8 }} name="Ligados" />
//         </LineChart>
//       </ResponsiveContainer>
//     </div>
//   );

//   return (
//     <div className="content-container">
//       {forecastChiller.length === 0 ? (
//         <div className="empty-message">
//           Acesse o menu lateral para parametrização!
//         </div>
//       ) : (
//         <>
//           {renderCorrenteVagLigadosChart()} {/* Gráfico combinado para Corrente, VAG e Ligados */}
//           {renderChart('delta_ac', 'Delta AC', '#8a2be2')}
//           {renderChart('tr', 'TR', '#ff6347')}
//           {renderChart('kwh', 'KWh', '#4682b4')}
//           {renderChart('torre', 'Frequência das torres (Hz)', '#20b2aa')}
//           {renderChart('temperatura', 'Temperatura (°C)', '#32cd32')}
//           {renderChart('pressao', 'Pressão (mbar)', '#ff4500')}
//           {renderChart('umidade', 'Umidade (%)', '#6495ed')}
//         </>
//       )}
//     </div>
//   );
// };

// export default Conteudo;

import './style.css';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface ForecastData {
  data_hora: string;
  corrente: number;
  vag: number;
  ligados: number;
  delta_ac: number;
  tr: number;
  kwh: number;
  temperatura: number;
  pressao: number;
  torre: number;
  umidade: number;
}

interface ConteudoProps {
  forecastChiller: ForecastData[];
  trainResult: any[]; // Novo estado para resultados do treinamento
}

const Conteudo: React.FC<ConteudoProps> = ({ forecastChiller, trainResult }) => {
  const data = forecastChiller.map((item) => ({
    dataHora: item.data_hora,
    corrente: item.corrente,
    vag: item.vag,
    ligados: item.ligados,
    delta_ac: item.delta_ac,
    tr: item.tr,
    kwh: item.kwh,
    temperatura: item.temperatura,
    pressao: item.pressao,
    torre: item.torre,
    umidade: item.umidade,
  }));

  const renderChart = (dataKey: keyof ForecastData, label: string, color: string) => (
    <div className="chart-wrapper">
      <h3>{label} ao Longo do Tempo</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="dataHora"
            tick={{ fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={70}
          />
          <YAxis
            label={{ value: label, angle: -90, position: 'insideLeft', offset: 0 }}
            tick={{ fontSize: 12 }}
          />
          <Tooltip formatter={(value: number) => `${value.toFixed(2)}`} />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey={dataKey} stroke={color} activeDot={{ r: 8 }} name={label} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );

  const renderCorrenteVagLigadosChart = () => (
    <div className="chart-wrapper">
      <h3>Análise de Corrente, VAG e Ligados ao Longo do Tempo</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="dataHora"
            tick={{ fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={70}
          />
          <YAxis
            label={{ value: 'Valores (%)', angle: -90, position: 'insideLeft', offset: 0 }}
            tick={{ fontSize: 12 }}
          />
          <Tooltip formatter={(value: number) => `${value.toFixed(2)}%`} />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="corrente" stroke="#8884d8" activeDot={{ r: 8 }} name="Corrente" />
          <Line type="monotone" dataKey="vag" stroke="#82ca9d" activeDot={{ r: 8 }} name="VAG" />
          <Line type="monotone" dataKey="ligados" stroke="#ff7300" activeDot={{ r: 8 }} name="Ligados" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );

  const renderTrainResultTable = () => (
    <div className="train-result">
      <h3>Resultados do Treinamento</h3>
      <table>
        <thead>
          <tr>
            {trainResult.length > 0 &&
              Object.keys(trainResult[0]).map((key) => <th key={key}>{key}</th>)}
          </tr>
        </thead>
        <tbody>
          {trainResult.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <div className="content-container">
      {forecastChiller.length === 0 && trainResult.length === 0 ? (
        <div className="empty-message">Acesse o menu lateral para parametrização!</div>
      ) : (
        <>
          {trainResult.length > 0 && renderTrainResultTable()}
          {forecastChiller.length > 0 && (
            <>
              {renderCorrenteVagLigadosChart()}
              {renderChart('delta_ac', 'Delta AC', '#8a2be2')}
              {renderChart('tr', 'TR', '#ff6347')}
              {renderChart('kwh', 'KWh', '#4682b4')}
              {renderChart('torre', 'Frequência das torres (Hz)', '#20b2aa')}
              {renderChart('temperatura', 'Temperatura (°C)', '#32cd32')}
              {renderChart('pressao', 'Pressão (mbar)', '#ff4500')}
              {renderChart('umidade', 'Umidade (%)', '#6495ed')}
            </>
          )}
        </>
      )}
    </div>
  );
};

export default Conteudo;
