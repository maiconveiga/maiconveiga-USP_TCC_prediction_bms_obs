#%% Tratamento Chiller
def tratarChiller(df):
    
    import pandas as pd
    import numpy as np
    
    # Função para preencher os valores NaN pela média dos vizinhos
    def preencher_media_vizinho_todas_colunas(df):
        # Iterar sobre cada coluna do DataFrame
        for column in df.columns:
            # Iterar sobre as linhas e substituir os valores NaN
            for i in range(1, len(df) - 1):
                if pd.isna(df.loc[i, column]):
                    # Substituir o NaN pela média entre a linha acima e a linha abaixo
                    df.loc[i, column] = (df.loc[i - 1, column] + df.loc[i + 1, column]) / 2
        return df
    
    df = preencher_media_vizinho_todas_colunas(df)
   
    df = df.dropna(subset=[col for col in df.columns if col not in ['UTCDateTime', 'ur_kwhtr']], how='all')
    
    # Substituir NaN em 'ur_correnteMotor' por 0, caso 'ur_kwh' seja 0
    df['ur_correnteMotor'] = df.apply(
        lambda row: 0 if pd.isna(row['ur_correnteMotor']) and row['ur_kwh'] == 0 else row['ur_correnteMotor'], axis=1
    )
    
    # Substituir 'ur_temp_saida' por 'ur_temp_entrada' se a temperatura de saída for menor que 0 e o kwh for 0
    df.loc[(df['ur_temp_saida'] < 0) & (df['ur_kwh'] == 0), 'ur_temp_saida'] = df['ur_temp_entrada']
    
    # Garantir que os valores de 'ur_kwhtr' não sejam negativos
    df.loc[df['ur_kwhtr'] < 0, 'ur_kwhtr'] = 0
    
    # Calcular a coluna TR e tratar infs e NaNs
    df['TR'] = df['ur_kwh'] / df['ur_kwhtr']
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df['TR'] = df['TR'].fillna(0)
    
    # Adicionar delta_AG e delta_AC
    df['delta_AG'] = df['ur_temp_entrada'] - df['ur_temp_saida']
    df['delta_AC'] = df['ur_temp_saida_condensacao'] - df['ur_temp_entrada_condensacao']
    
    # Marcar finais de semana
    df['FimDeSemana'] = df['UTCDateTime'].apply(lambda x: 1 if x.weekday() >= 5 else 0)

    # Marcar horários comerciais
    df['HorarioComercial'] = df['UTCDateTime'].apply(lambda x: 1 if 8 <= x.hour < 17 else 0)

    return df

#%% Tratamento Fancoil
def tratarFancoil(df):
    
    import pandas as pd
    
    # Remover linhas onde todas as colunas, exceto 'UTCDateTime', são NaN
  
    # Função para preencher os valores NaN pela média dos vizinhos
    def preencher_media_vizinho_todas_colunas(df):
        for column in df.columns:
            for i in range(1, len(df) - 1):
                if pd.isna(df.loc[i, column]):
                    df.loc[i, column] = (df.loc[i - 1, column] + df.loc[i + 1, column]) / 2
        return df
    
    df = preencher_media_vizinho_todas_colunas(df)
    df = df.dropna(subset=[col for col in df.columns if col != 'UTCDateTime'], how='all')
  
    # Calcular porcentagem de 'VAG Aberta %'
    df['VAG_Aberta_%'] = df.drop(columns=['UTCDateTime']).sum(axis=1) / (df.shape[1] - 1)
    
    # Calcular porcentagem de 'Fancoil ligado %'
    df['Fancoil_ligado_%'] = (((df.shape[1] - 1) - df.drop(columns=['UTCDateTime']).apply(lambda row: (row == 0).sum(), axis=1)) * 100) / (df.shape[1] - 1)

    return df

#%% Tratamento CAG
def tratarCAG(df):
    
    # Preencher NaNs em 'Torre_1', 'Torre_2' e 'Torre_3' com a média das três
    df[['Torre_1', 'Torre_2', 'Torre_3']] = df[['Torre_1', 'Torre_2', 'Torre_3']].apply(
        lambda x: x.fillna(x.mean()), axis=1
    )
    
    return df
#%% Trata AHU
def tratarAHU(df):
    # Remove colunas que contêm apenas NaN
    df = df.dropna(axis=1, how='all')
    
    # Aplica o preenchimento de NaN com a média das linhas acima e abaixo somente nas colunas numéricas
    for col in df.select_dtypes(include=[float, int]).columns:
        df[col] = df[col].fillna((df[col].shift(1) + df[col].shift(-1)) / 2)
    
    # Remove linhas que ainda possam ter NaN após o preenchimento
    df = df.dropna()
    # Marcar finais de semana
    df['FimDeSemana'] = df['UTCDateTime'].apply(lambda x: 1 if x.weekday() >= 5 else 0)

    # Marcar horários comerciais
    df['HorarioComercial'] = df['UTCDateTime'].apply(lambda x: 1 if 8 <= x.hour < 17 else 0)

    
    return df
