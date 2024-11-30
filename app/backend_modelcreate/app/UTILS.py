# #%% Conexão com o banco
# def conexaoBanco():
    
#     from sqlalchemy import create_engine

#     #Dados para inserir
#     machine = 'M5282650'
#     instance = 'SQLEXPRESS'
#     username = 'py'
#     password = 'py'
    
#     server = f'{machine}\\{instance}'
#     database = 'JCIHistorianDB'
#     connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
#     engine = create_engine(connection_string)
#     return engine

# #%% Listagem de pontos
# def getListaEquipamentos():

#     import pandas as pd

#     # Função de conexão com o banco de dados
#     engine = conexaoBanco()
    
#     # Query para obter os dados
#     query = """
#     SELECT DISTINCT PointName
#     FROM [JCIHistorianDB].[dbo].[RawAnalog]
#     """
#     df = pd.read_sql(query, engine)
#     df['Tipo'] = ''
#     df['Equipamento'] = ''
#     df['Ponto'] = ''
    
#     # Salvar o DataFrame como um arquivo Excel
#     df.to_csv('Lista_Pontos_Equipamento.csv', index=False)
 
# def juntarDF(df_UR, df_VAG, df_CAG):
#     import pandas as pd
    
#     # Colunas escolhidas de df_VAG
#     colunas_para_juntar_VAG = ['UTCDateTime', 'VAG_Aberta_%', 'Fancoil_ligado_%']  # Inclua 'UTCDateTime' para o merge
    
#     # Realiza o merge entre df_UR e as colunas específicas de df_VAG com base em 'UTCDateTime'
#     df = pd.merge(df_UR, df_VAG[colunas_para_juntar_VAG], on='UTCDateTime', how='left') 
    
#     # Realiza o merge entre o resultado anterior e df_CAG com base em 'UTCDateTime'
#     df = pd.merge(df, df_CAG, on='UTCDateTime', how='inner')
    
#     # Se necessário, pode remover valores NaN após a junção
#     # df = df.dropna()
    
#     return df

# def juntarAHUCAG(df_AHU, df_CAG):
#     import pandas as pd
    
#     # Realiza o merge entre o resultado anterior e df_CAG com base em 'UTCDateTime'
#     df = pd.merge(df_AHU, df_CAG, on='UTCDateTime', how='inner')
    
#     # Se necessário, pode remover valores NaN após a junção
#     # df = df.dropna()
    
#     return df

import pyodbc
import pandas as pd

# Função de conexão com o banco de dados usando pyodbc
def conexaoBanco():
    server = '192.168.0.11'
    database = 'JCIHistorianDB'
    username = 'py'
    password = 'py'

    # Corrija o nome do driver para o correto
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        conn = pyodbc.connect(connection_string)
        print("Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

# Listagem de pontos, agora usando pyodbc para a conexão
def getListaEquipamentos():
    # Conectar ao banco de dados
    conn = conexaoBanco()
    if conn is None:
        return
    
    # Query para obter os dados
    query = """
    SELECT DISTINCT PointName
    FROM [JCIHistorianDB].[dbo].[RawAnalog]
    """
    
    # Carregar os dados para o DataFrame
    df = pd.read_sql(query, conn)
    
    # Adicionar colunas extras conforme necessário
    df['Tipo'] = ''
    df['Equipamento'] = ''
    df['Ponto'] = ''
    
    # Salvar o DataFrame como um arquivo CSV
    df.to_csv('Lista_Pontos_Equipamento.csv', index=False)
    
    # Fechar a conexão
    conn.close()

# Função de junção de DataFrames (sem alteração necessária)
def juntarDF(df_UR, df_VAG, df_CAG):
    # Colunas escolhidas de df_VAG
    colunas_para_juntar_VAG = ['UTCDateTime', 'VAG_Aberta_%', 'Fancoil_ligado_%']
    
    # Realiza o merge entre df_UR e as colunas específicas de df_VAG com base em 'UTCDateTime'
    df = pd.merge(df_UR, df_VAG[colunas_para_juntar_VAG], on='UTCDateTime', how='left')
    
    # Realiza o merge entre o resultado anterior e df_CAG com base em 'UTCDateTime'
    df = pd.merge(df, df_CAG, on='UTCDateTime', how='inner')
    
    return df

# Função de junção de AHU com CAG (sem alteração necessária)
def juntarAHUCAG(df_AHU, df_CAG):
    df = pd.merge(df_AHU, df_CAG, on='UTCDateTime', how='inner')
    return df
