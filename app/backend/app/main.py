from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import httpx
from tensorflow.keras.models import load_model
import os
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from app.config import settings
from app.config import logger
import asyncio

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = FastAPI()

# Configuração do Elastic APM
apm = make_apm_client(
    {
        "SERVICE_NAME": "backend_predict",
        "DEBUG": True,
        "SERVER_URL": "http://apm:8200",
        "ENVIRONMENT": "development",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ElasticAPM, client=apm)

logger.debug("Elastic APM client initialized: %s", apm)

# Configurações e variáveis globais
cidade = settings.CIDADE
api_key = settings.API_KEY
tempo_atualizacao_clima = timedelta(minutes=10)
dados_clima_cache = None
ultima_atualizacao_clima = datetime.min

modelos_scalers_cache = {}

@app.on_event("startup")
def carregar_todos_modelos():
    """
    Pré-carrega todos os modelos e scalers ao iniciar a aplicação.
    """
    logger.debug("Carregando todos os modelos e scalers...")
    carregar_modelos_scalers(1)
    carregar_modelos_scalers(2)
    logger.debug("Modelos e scalers carregados.")

def carregar_modelo(joblib_path, keras_path):
    """
    Carrega um modelo TensorFlow (.h5) ou Scikit-learn (.pkl).
    """
    if os.path.exists(keras_path):
        return load_model(keras_path)
    elif os.path.exists(joblib_path):
        return joblib.load(joblib_path)
    else:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")

def carregar_modelos_scalers(chiller_num):
    """
    Carrega modelos e scalers para um chiller específico (1 ou 2).
    """
    if chiller_num not in modelos_scalers_cache:
        pathProd = f'app/models/chiller{chiller_num}/'
        modelos_scalers_cache[chiller_num] = {
            'corrente': (carregar_modelo(f'{pathProd}ur_correnteMotor/model.pkl', f'{pathProd}ur_correnteMotor/model.h5'), joblib.load(f'{pathProd}ur_correnteMotor/scaler.pkl')),
            'ligados': (carregar_modelo(f'{pathProd}Fancoil_ligado_%/model.pkl', f'{pathProd}Fancoil_ligado_%/model.h5'), joblib.load(f'{pathProd}Fancoil_ligado_%/scaler.pkl')),
            'vag': (carregar_modelo(f'{pathProd}VAG_Aberta_%/model.pkl', f'{pathProd}VAG_Aberta_%/model.h5'), joblib.load(f'{pathProd}VAG_Aberta_%/scaler.pkl')),
            'deltaAC': (carregar_modelo(f'{pathProd}delta_AC/model.pkl', f'{pathProd}delta_AC/model.h5'), joblib.load(f'{pathProd}delta_AC/scaler.pkl')),
            'TR': (carregar_modelo(f'{pathProd}TR/model.pkl', f'{pathProd}TR/model.h5'), joblib.load(f'{pathProd}TR/scaler.pkl')),
            'KWH': (carregar_modelo(f'{pathProd}ur_kwh/model.pkl', f'{pathProd}ur_kwh/model.h5'), joblib.load(f'{pathProd}ur_kwh/scaler.pkl')),
            'torre3': (carregar_modelo(f'{pathProd}Torre_3/model.pkl', f'{pathProd}Torre_3/model.h5'), joblib.load(f'{pathProd}Torre_3/scaler.pkl'))
        }
    return modelos_scalers_cache[chiller_num]

async def obter_dados_climaticos():
    """
    Obtém dados climáticos da API OpenWeather, com cache e atualização a cada 10 minutos.
    """
    global dados_clima_cache, ultima_atualizacao_clima
    if datetime.now() - ultima_atualizacao_clima > tempo_atualizacao_clima:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric"
            async with httpx.AsyncClient(verify=False) as client:
                resposta = await client.get(url)
                resposta.raise_for_status()
                dados_clima = resposta.json()
                dados_clima_cache = (
                    dados_clima['main']['pressure'],
                    dados_clima['main']['humidity'],
                    dados_clima['main']['temp']
                )
                ultima_atualizacao_clima = datetime.now()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao obter dados climáticos: {e}")
    return dados_clima_cache

async def obter_previsao_climatica():
    """
    Obtém a previsão climática da API OpenWeather para múltiplos registros.
    """
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={api_key}&units=metric'
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url)
        response.raise_for_status()
        dados = response.json()

        return [
            {
                "UTCDateTime": registro["dt"],
                "temperatura": registro["main"]["temp"],
                "pressao": registro["main"]["pressure"],
                "umidade": registro["main"]["humidity"]
            }
            for registro in dados["list"]
        ]

def verificar_data_horario():
    """
    Verifica se a data atual é final de semana e horário comercial.
    """
    data_hora = datetime.now()
    return 1 if data_hora.weekday() >= 5 else 0, 1 if 8 <= data_hora.hour < 17 else 0

def verificar_data_horario_prev(data_hora_prev):
    """
    Verifica se a data passada é final de semana e horário comercial.
    """
    data_hora_prev = datetime.utcfromtimestamp(data_hora_prev)
    return 1 if data_hora_prev.weekday() >= 5 else 0, 1 if 8 <= data_hora_prev.hour < 17 else 0

async def calcular_previsoes_async(scaler, model, *args):
    """
    Calcula previsões de forma assíncrona.
    """
    input_data = np.array([args])
    input_data_scaled = scaler.transform(input_data)
    return model.predict(input_data_scaled).flatten()[0]

# Classe de entrada
class PrevisaoInput(BaseModel):
    ur_temp_saida: float
    chiller: int

# Classe de saída
class PrevisaoOutput(BaseModel):
    corrente: float
    vag: float
    ligados: float
    delta_ac: float
    tr: float
    kwh: float
    torre: float
    temperatura: float
    pressao: float
    umidade: float
    horario_comercial: int
    fim_de_semana: int
    data_hora: str

@app.get("/")
async def root():
    return {"message": "API Predict em operação"}


@app.post("/actual/chiller", response_model=PrevisaoOutput)
async def previsao_chiller(dados: PrevisaoInput):
    """
    Endpoint para calcular previsões de um chiller específico.
    """
    try:
        if dados.chiller not in [1, 2]:
            raise HTTPException(status_code=400, detail="Chiller inválido. Escolha 1 ou 2.")
        modelos_scalers = carregar_modelos_scalers(dados.chiller)
        pressao, umidade, temperatura = await obter_dados_climaticos()
        fim_de_semana, horario_comercial = verificar_data_horario()

        previsoes = await asyncio.gather(
            calcular_previsoes_async(modelos_scalers['ligados'][1], modelos_scalers['ligados'][0], pressao, temperatura, umidade, fim_de_semana, horario_comercial),
            calcular_previsoes_async(modelos_scalers['vag'][1], modelos_scalers['vag'][0], pressao, temperatura, umidade, fim_de_semana, horario_comercial),
            calcular_previsoes_async(modelos_scalers['deltaAC'][1], modelos_scalers['deltaAC'][0], pressao, temperatura, umidade, dados.ur_temp_saida),
            calcular_previsoes_async(modelos_scalers['TR'][1], modelos_scalers['TR'][0], pressao, temperatura, umidade, dados.ur_temp_saida, fim_de_semana, horario_comercial),
            calcular_previsoes_async(modelos_scalers['KWH'][1], modelos_scalers['KWH'][0], pressao, temperatura, umidade, dados.ur_temp_saida),
            calcular_previsoes_async(modelos_scalers['corrente'][1], modelos_scalers['corrente'][0], pressao, temperatura, umidade, dados.ur_temp_saida)
        )

        return PrevisaoOutput(
            corrente=previsoes[5],
            vag=previsoes[1],
            ligados=previsoes[0],
            delta_ac=previsoes[2],
            tr=previsoes[3],
            kwh=previsoes[4],
            torre=0.0,
            temperatura=temperatura,
            pressao=pressao,
            umidade=umidade,
            horario_comercial=horario_comercial,
            fim_de_semana=fim_de_semana,
            data_hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/forecast/chiller", response_model=list[PrevisaoOutput])
async def previsao_chiller_forecast(dados: PrevisaoInput):
    """
    Endpoint para calcular previsões futuras para um chiller específico.
    """
    try:
        if dados.chiller not in [1, 2]:
            raise HTTPException(status_code=400, detail="Chiller inválido. Escolha 1 ou 2.")
        previsao_clima = await obter_previsao_climatica()

        if not previsao_clima:
            raise HTTPException(status_code=500, detail="Erro ao obter previsão climática.")

        modelos_scalers = carregar_modelos_scalers(dados.chiller)
        previsoes = []

        for clima in previsao_clima:
            fim_de_semana, horario_comercial = verificar_data_horario_prev(clima["UTCDateTime"])
            pressao, temperatura, umidade = clima["pressao"], clima["temperatura"], clima["umidade"]

            previsaoLigados = await calcular_previsoes_async(
                modelos_scalers['ligados'][1], modelos_scalers['ligados'][0],
                pressao, temperatura, umidade, fim_de_semana, horario_comercial
            )
            previsaoVAG = await calcular_previsoes_async(
                modelos_scalers['vag'][1], modelos_scalers['vag'][0],
                pressao, temperatura, umidade, fim_de_semana, horario_comercial, previsaoLigados
            )
            previsaodeltaAC = await calcular_previsoes_async(
                modelos_scalers['deltaAC'][1], modelos_scalers['deltaAC'][0],
                pressao, temperatura, umidade, dados.ur_temp_saida, previsaoVAG, previsaoLigados
            )
            previsaoTorre3 = await calcular_previsoes_async(
                modelos_scalers['torre3'][1], modelos_scalers['torre3'][0],
                pressao, temperatura, umidade, previsaodeltaAC, previsaoVAG
            )
            previsaoTR = await calcular_previsoes_async(
                modelos_scalers['TR'][1], modelos_scalers['TR'][0],
                pressao, temperatura, umidade, previsaodeltaAC, previsaoVAG,
                dados.ur_temp_saida, fim_de_semana, horario_comercial, previsaoLigados, previsaoTorre3
            )
            previsaoKWH = await calcular_previsoes_async(
                modelos_scalers['KWH'][1], modelos_scalers['KWH'][0],
                pressao, temperatura, umidade, previsaodeltaAC, previsaoTR,
                dados.ur_temp_saida, previsaoVAG, previsaoTorre3, previsaoLigados
            )
            previsaoCorrente = await calcular_previsoes_async(
                modelos_scalers['corrente'][1], modelos_scalers['corrente'][0],
                pressao, temperatura, umidade, dados.ur_temp_saida, previsaoTR,
                previsaodeltaAC, previsaoVAG, previsaoLigados, previsaoKWH, previsaoTorre3
            )

            previsoes.append(
                PrevisaoOutput(
                    corrente=previsaoCorrente,
                    vag=previsaoVAG,
                    ligados=previsaoLigados,
                    delta_ac=previsaodeltaAC,
                    tr=previsaoTR,
                    kwh=previsaoKWH,
                    torre=previsaoTorre3,
                    temperatura=temperatura,
                    pressao=pressao,
                    umidade=umidade,
                    horario_comercial=horario_comercial,
                    fim_de_semana=fim_de_semana,
                    data_hora=datetime.utcfromtimestamp(clima["UTCDateTime"]).strftime("%Y-%m-%d %H:%M:%S")
                )
            )

        return previsoes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
