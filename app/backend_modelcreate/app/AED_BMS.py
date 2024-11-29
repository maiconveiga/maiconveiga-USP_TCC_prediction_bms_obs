def getBMS():
    import pandas as pd
    from app.UTILS import conexaoBanco
    from pathlib import Path
    #%% Conexão
    
    #%% Leitura do arquivo    
    file_path = Path("app/Dados/Lista_Pontos.xlsx")
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df_lista = pd.read_excel(file_path)

    engine = conexaoBanco()
    
    #%% Coleta
    
    # Criar um dicionário para armazenar os DataFrames de cada equipamento
    dfs_equipamentos = {}
    
    # Obter o UTCDateTime mínimo e máximo da primeira query
    for i, row in df_lista.iterrows():
        point_name = row['PointName']  # Nome do ponto no banco de dados
        
        # Construção da query para obter o UTCDateTime máximo e mínimo
        query = f"""
        SELECT MIN(UTCDateTime) AS Min_UTCDateTime, 
               MAX(UTCDateTime) AS Max_UTCDateTime
        FROM [JCIHistorianDB].[dbo].[RawAnalog]
        WHERE PointName = '{point_name}'
        """
        
        # Executar a query e armazenar os resultados
        df_temp = pd.read_sql(query, engine)
        
        # Exibir os resultados (opcional)
        min_datetime = pd.to_datetime(df_temp['Min_UTCDateTime'][0])
        max_datetime = pd.to_datetime(df_temp['Max_UTCDateTime'][0])
        
        break  # Faz a coleta do primeiro ponto apenas para pegar min e max UTCDateTime

    # Gerar um índice de 30 minutos com base nos valores mínimos e máximos
    index = pd.date_range(start=min_datetime, end=max_datetime, freq='15min')

    # Criar DataFrames vazios para cada equipamento
    equipamentos = df_lista['Equipamento'].unique()  # Lista de equipamentos únicos
    
    for equipamento in equipamentos:
        # Inicializar um DataFrame vazio para cada equipamento
        dfs_equipamentos[equipamento] = pd.DataFrame(index=index)
    
    # Loop através dos nomes dos pontos para coletar os dados e organizá-los por equipamento
    for i, row in df_lista.iterrows():
        point_name = row['PointName']  # Nome na base de dados
        nome_ponto = row['Ponto']  # Nome da coluna "Ponto" no Excel
        equipamento = row['Equipamento']  # Nome do equipamento

        # Construção da query
        query = f"""
        SELECT UTCDateTime, PointName, ActualValue 
        FROM [JCIHistorianDB].[dbo].[RawAnalog] 
        WHERE PointName = '{point_name}'
        """
        
        # Executando a query e armazenando o resultado em um DataFrame temporário
        df_temp = pd.read_sql(query, engine)
        
        # Converta a coluna UTCDateTime para datetime
        df_temp['UTCDateTime'] = pd.to_datetime(df_temp['UTCDateTime'])
        
        # Renomear a coluna 'ActualValue' para o valor da coluna 'Ponto'
        df_temp = df_temp.rename(columns={'ActualValue': nome_ponto})
        
        # Deletar a coluna 'PointName'
        df_temp = df_temp.drop(columns=['PointName'])
        
        # Definir UTCDateTime como índice
        df_temp.set_index('UTCDateTime', inplace=True)
        
        # Mesclar os dados no DataFrame correspondente ao equipamento
        dfs_equipamentos[equipamento] = dfs_equipamentos[equipamento].merge(
            df_temp, how='left', left_index=True, right_index=True
        )
    
    # Preencher os valores NaN para cada DataFrame de equipamento
    for equipamento in dfs_equipamentos:
        dfs_equipamentos[equipamento] = dfs_equipamentos[equipamento].reset_index()
        dfs_equipamentos[equipamento] = dfs_equipamentos[equipamento].rename(columns={'index': 'UTCDateTime'})

    return dfs_equipamentos
