from fastapi import FastAPI
from app.AED_Tratar import tratarChiller, tratarFancoil, tratarCAG, tratarAHU
from app.AED_BMS import getBMS
from app.UTILS import getListaEquipamentos, juntarDF, juntarAHUCAG
from app.EAD_Meteorologico import DadosMeteorologicos
from app.model import Prever
import pandas as pd
import threading 
# from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
# from app.config import logger
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configuração do Elastic APM
# apm = make_apm_client(
#     {
#         "SERVICE_NAME": "backend_train",
#         "DEBUG": True,
#         "SERVER_URL": "http://apm:8200",
#         "ENVIRONMENT": "development",
#     }
# )

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(ElasticAPM, client=apm)

# logger.debug("Elastic APM client initialized: %s", apm)

class TrainRequest(BaseModel):
    siteID: int
    siteName: str


# Variável global para armazenar os DataFrames
class DataFrameStorage:
    def __init__(self):
        self.lock = threading.Lock()
        self.dataframes: Dict[str, pd.DataFrame] = {}

    def set(self, key: str, df: pd.DataFrame):
        with self.lock:
            self.dataframes[key] = df

    def get(self, key: str) -> pd.DataFrame:
        with self.lock:
            return self.dataframes.get(key)

df_storage = DataFrameStorage()

@app.get("/")
async def root():
    return {"message": "API Train em operação!"}


# @app.post("/generate-graphs")
# def generate_graphs():
#     """
#     Endpoint para gerar gráficos dos DataFrames e retornar no formato JSON.
#     """
#     from io import BytesIO
#     import base64
#     import matplotlib.pyplot as plt
#     import seaborn as sns

#     df_all = getBMS()

#     for key, df in df_all.items():
#         df_storage.set(key, df)

#     for e in df_all.keys():
#         if 'chiller' in e.lower():
#             df_all[e] = tratarChiller(df_all[e])
#         elif 'fancoil' in e.lower():
#             df_all[e] = tratarFancoil(df_all[e])
#         elif 'cag' in e.lower():
#             df_all[e] = tratarCAG(df_all[e])
#         elif 'ahu' in e.lower():
#             df_all[e] = tratarAHU(df_all[e])

#     for e in df_all.keys():
#         if 'chiller' in e.lower():
#             for e_b in df_all.keys():
#                 if 'fancoil' in e_b.lower():
#                     for e_c in df_all.keys():
#                         if 'cag' in e_c.lower():
#                             df_all[e] = juntarDF(df_all[e], df_all[e_b], df_all[e_c])

#     for e in df_all.keys():
#         if 'ahu' in e.lower():
#             for e_b in df_all.keys():
#                 if 'cag' in e_b.lower():
#                     df_all[e] = juntarAHUCAG(df_all[e], df_all[e_b])

#     for e in df_all.keys():
#         if 'chiller' in e.lower():
#             df_all[e] = DadosMeteorologicos(df_all[e])
#         elif 'ahu' in e.lower():
#             df_all[e] = DadosMeteorologicos(df_all[e])

#     for e in df_all.keys():
#         if 'chiller' in e.lower():
#             df_all[e] = df_all[e].dropna()
#         elif 'ahu' in e.lower():
#             df_all[e] = df_all[e].dropna()

#     results = {}
#     for key, df in df_all.items():
#         if 'chiller' in key.lower() or 'ahu' in key.lower():
#             results[key] = {}

#             # Histogram
#             hist_img = BytesIO()
#             df.drop(columns=['UTCDateTime', 'FimDeSemana', 'HorarioComercial'], errors='ignore').hist(
#                 figsize=(10, 8), bins=40, edgecolor='black'
#             )
#             plt.tight_layout()
#             plt.savefig(hist_img, format='png')
#             plt.close()
#             results[key]['histogram'] = base64.b64encode(hist_img.getvalue()).decode('utf-8')

#             # Boxplot
#             boxplot_img = BytesIO()
#             sns.boxplot(data=df.drop(columns=['UTCDateTime', 'FimDeSemana', 'HorarioComercial'], errors='ignore'))
#             plt.title(f"Boxplot - {key}")
#             plt.tight_layout()
#             plt.savefig(boxplot_img, format='png')
#             plt.close()
#             results[key]['boxplot'] = base64.b64encode(boxplot_img.getvalue()).decode('utf-8')

#     return {
#         "message": "Graphs generated successfully.",
#         "graphs": results
#     }


@app.post("/pointlist")
def generate_pointlist():
    """
    Endpoint para gerar a lista de pontos do sistema.
    """
    getListaEquipamentos()
    return {"message": "Pointlist generated successfully."}

@app.post("/train")
def train_models(request: TrainRequest):
    """
    Endpoint para coletar e tratar os dados do sistema. Depois realiza o treinamento.
    """
    siteID = request.siteID
    siteName = request.siteName

    df_all = getBMS()

    for key, df in df_all.items():
        df_storage.set(key, df)

    for e in df_all.keys():
        if 'chiller' in e.lower():
            df_all[e] = tratarChiller(df_all[e])
        elif 'fancoil' in e.lower():
            df_all[e] = tratarFancoil(df_all[e])
        elif 'cag' in e.lower():
            df_all[e] = tratarCAG(df_all[e])
        elif 'ahu' in e.lower():
            df_all[e] = tratarAHU(df_all[e])

    for e in df_all.keys():
        if 'chiller' in e.lower():
            for e_b in df_all.keys():
                if 'fancoil' in e_b.lower():
                    for e_c in df_all.keys():
                        if 'cag' in e_c.lower():
                            df_all[e] = juntarDF(df_all[e], df_all[e_b], df_all[e_c])

    for e in df_all.keys():
        if 'ahu' in e.lower():
            for e_b in df_all.keys():
                if 'cag' in e_b.lower():
                    df_all[e] = juntarAHUCAG(df_all[e], df_all[e_b])

    for e in df_all.keys():
        if 'chiller' in e.lower():
            df_all[e] = DadosMeteorologicos(df_all[e])
        elif 'ahu' in e.lower():
            df_all[e] = DadosMeteorologicos(df_all[e])

    for e in df_all.keys():
        if 'chiller' in e.lower():
            df_all[e] = df_all[e].dropna()
        elif 'ahu' in e.lower():
            df_all[e] = df_all[e].dropna()

    results = {}

    for e in df_all.keys():
        if 'chiller' in e.lower():
            results[e] = []
            # VAG Aberta
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)', 'FimDeSemana', 'HorarioComercial', 'Fancoil_ligado_%']
            y_col = 'VAG_Aberta_%'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

            # Delta AC
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)', 'ur_temp_saida','VAG_Aberta_%','Fancoil_ligado_%']
            y_col = 'delta_AC'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

            # KWh
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','delta_AC','TR','ur_temp_saida','VAG_Aberta_%','Torre_3','Fancoil_ligado_%']
            y_col = 'ur_kwh'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

            # Fancoil ligado %
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','FimDeSemana','HorarioComercial']
            y_col = 'Fancoil_ligado_%'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

            # TR
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','delta_AC', 'VAG_Aberta_%', 'ur_temp_saida', 'FimDeSemana', 'HorarioComercial', 'Fancoil_ligado_%', 'Torre_3']
            y_col = 'TR'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

            # Corrente
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)', 'ur_temp_saida', 'TR', 'delta_AC', 'VAG_Aberta_%', 'Fancoil_ligado_%', 'ur_kwh', 'Torre_3']
            y_col = 'ur_correnteMotor'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

            # Torre 1
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','delta_AC','VAG_Aberta_%']
            y_col = 'Torre_1'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))
   
            # Torre 2
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','delta_AC','VAG_Aberta_%']
            y_col = 'Torre_2'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

            # Torre 3
            X = ['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','delta_AC','VAG_Aberta_%']
            y_col = 'Torre_3'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

        elif 'ahu' in e.lower():
            results[e] = []
            # AHU-03-02
            X = ['Pressao (mB)', 'Temperatura (°C)', 'TI', 'VAG']
            y_col = 'STA_media'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))
            # AHU-03-02
            X = ['VAG', 'FimDeSemana']
            y_col = 'TI'
            results[e].append(Prever(siteID, siteName, df_all[e], e, X, y_col))

    return {"Site ID":siteID, "Site Name":siteName, "results": results}
