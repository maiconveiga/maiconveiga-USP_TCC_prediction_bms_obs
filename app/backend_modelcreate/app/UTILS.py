#%% Conexão com o banco
def conexaoBanco():
    
    from sqlalchemy import create_engine
    
    #Dados para inserir
    # machine = 'M5282650'
    machine = '172.30.208.1'
    instance = 'SQLEXPRESS'
    username = 'py'
    password = 'py'
    
    server = f'{machine}\\{instance}'
    database = 'JCIHistorianDB'
    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
    engine = create_engine(connection_string)
    return engine

#%% Listagem de pontos
def getListaEquipamentos():

    import pandas as pd

    # Função de conexão com o banco de dados
    engine = conexaoBanco()
    
    # Query para obter os dados
    query = """
    SELECT DISTINCT PointName
    FROM [JCIHistorianDB].[dbo].[RawAnalog]
    """
    df = pd.read_sql(query, engine)
    df['Tipo'] = ''
    df['Equipamento'] = ''
    df['Ponto'] = ''
    
    # Salvar o DataFrame como um arquivo Excel
    df.to_csv('Lista_Pontos_Equipamento.csv', index=False)
 
def juntarDF(df_UR, df_VAG, df_CAG):
    import pandas as pd
    
    # Colunas escolhidas de df_VAG
    colunas_para_juntar_VAG = ['UTCDateTime', 'VAG_Aberta_%', 'Fancoil_ligado_%']  # Inclua 'UTCDateTime' para o merge
    
    # Realiza o merge entre df_UR e as colunas específicas de df_VAG com base em 'UTCDateTime'
    df = pd.merge(df_UR, df_VAG[colunas_para_juntar_VAG], on='UTCDateTime', how='left') 
    
    # Realiza o merge entre o resultado anterior e df_CAG com base em 'UTCDateTime'
    df = pd.merge(df, df_CAG, on='UTCDateTime', how='inner')
    
    # Se necessário, pode remover valores NaN após a junção
    # df = df.dropna()
    
    return df

def juntarAHUCAG(df_AHU, df_CAG):
    import pandas as pd
    
    # Realiza o merge entre o resultado anterior e df_CAG com base em 'UTCDateTime'
    df = pd.merge(df_AHU, df_CAG, on='UTCDateTime', how='inner')
    
    # Se necessário, pode remover valores NaN após a junção
    # df = df.dropna()
    
    return df
