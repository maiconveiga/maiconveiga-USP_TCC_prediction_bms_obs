# def Prever(siteID, siteName, df, chiller, X, y_col):    
#     import pandas as pd
#     from sklearn.model_selection import train_test_split
#     from sklearn.preprocessing import StandardScaler
#     from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
#     # from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, Lasso
#     from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor#, AdaBoostRegressor
#     from sklearn.svm import SVR
#     # import xgboost as xgb
#     # import lightgbm as lgb
#     # from catboost import CatBoostRegressor
#     from tensorflow.keras.models import Sequential
#     from tensorflow.keras.layers import Dense
#     from tensorflow.keras.optimizers import Adam
#     from tensorflow.keras.callbacks import EarlyStopping
#     # from sklearn.neighbors import KNeighborsRegressor
#     import sqlite3
#     import pickle
#     from datetime import datetime
#     import joblib
#     import os

#     modelPath = f'ModelsDeploy/{siteID}_{siteName}/{chiller}/{y_col}'
#     # Criação do diretório para salvar o modelo e scaler
#     os.makedirs(modelPath, exist_ok=True)

#     def save_to_db(chiller, y_col, model, scaler, model_name):
#         """
#         Função para salvar o modelo e scaler no banco de dados SQLite.
#         """
#         conn = sqlite3.connect("models.db")
#         cursor = conn.cursor()

#         # Criar tabela, se ainda não existir
#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Models (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             siteID INTEGER NOT NULL,
#             siteName TEXT NOT NULL,
#             chiller TEXT NOT NULL,
#             y_col TEXT NOT NULL,
#             model_name TEXT NOT NULL,
#             model_data BLOB NOT NULL,
#             scaler_data BLOB NOT NULL,
#             created_at TEXT NOT NULL
#         );
#         """)

#         # Serializar modelo e scaler
#         model_data = pickle.dumps(model)
#         scaler_data = pickle.dumps(scaler)

#         # Inserir no banco de dados
#         query = """
#         INSERT INTO Models (siteID, siteName, chiller, y_col, model_name, model_data, scaler_data, created_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?);
#         """
#         cursor.execute(query, (siteID, siteName, chiller, y_col, model_name, model_data, scaler_data, datetime.now()))
#         conn.commit()

#         cursor.close()
#         conn.close()

#     # Separando as features (X) e o target (y)
#     X = df[X]
#     y = df[y_col]

#     # Dividindo o dataset em treino e teste
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

#     # Normalizando os dados
#     scaler = StandardScaler()
#     X_train = scaler.fit_transform(X_train)
#     X_test = scaler.transform(X_test)

#     # Modelos a serem avaliados
#     modelos = {
#         # 'Linear': LinearRegression(),
#         # 'Ridge': Ridge(alpha=1.0),
#         # 'Lasso': Lasso(alpha=1.0),
#         # 'ElasticNet': ElasticNet(alpha=1.0, l1_ratio=0.5),
#         'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
#         'Extra Trees': ExtraTreesRegressor(n_estimators=100, random_state=42),
#         'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
#         # 'AdaBoost': AdaBoostRegressor(n_estimators=100, random_state=42),
#         # 'KNeighbors': KNeighborsRegressor(n_neighbors=5),
#         # 'SVR': SVR(kernel='rbf'),
#         # 'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42),
#         # 'LightGBM': lgb.LGBMRegressor(n_estimators=100, random_state=42),
#         # 'CatBoost': CatBoostRegressor(n_estimators=100, random_state=42, verbose=0)
#     }

#     # Avaliação dos modelos
#     resultados = []
#     for nome, modelo in modelos.items():
#         modelo.fit(X_train, y_train)
#         y_pred = modelo.predict(X_test)
#         mse = mean_squared_error(y_test, y_pred)
#         r2 = r2_score(y_test, y_pred)
#         mae = mean_absolute_error(y_test, y_pred)
#         resultados.append([nome, mse, r2, mae])
#         print(f'{nome}: MSE={mse:.4f}, R²={r2:.4f}, MAE={mae:.4f}')

#     # Avaliação da Rede Neural
#     model_nn = Sequential([
#         Dense(64, input_dim=X_train.shape[1], activation='relu'),
#         Dense(32, activation='relu'),
#         Dense(16, activation='relu'),
#         Dense(1, activation='linear')
#     ])
#     model_nn.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
#     early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
#     model_nn.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=32, callbacks=[early_stopping], verbose=0)
#     y_pred_nn = model_nn.predict(X_test).flatten()

#     # Métricas da rede neural
#     mse_nn = mean_squared_error(y_test, y_pred_nn)
#     r2_nn = r2_score(y_test, y_pred_nn)
#     mae_nn = mean_absolute_error(y_test, y_pred_nn)
#     resultados.append(['Neural Network', mse_nn, r2_nn, mae_nn])
#     print(f'Neural Network: MSE={mse_nn:.4f}, R²={r2_nn:.4f}, MAE={mae_nn:.4f}')

#     # Criação da tabela de resultados com 4 casas decimais
#     df_resultados = pd.DataFrame(resultados, columns=['Modelo', 'MSE', 'R²', 'MAE'])
#     df_resultados[['MSE', 'R²', 'MAE']] = df_resultados[['MSE', 'R²', 'MAE']].applymap(lambda x: f"{x:.4f}")

#     # Eleger o melhor modelo com base no R²
#     indice_melhor_modelo = df_resultados['R²'].astype(float).idxmax()
#     melhor_modelo = df_resultados.loc[indice_melhor_modelo, 'Modelo']
#     print(f'Melhor modelo: {melhor_modelo}')

#     # Salvar o melhor modelo e o scaler no banco
#     if melhor_modelo == 'Neural Network':
#         save_to_db(chiller, y_col, model_nn, scaler, 'Neural Network')
#     else:
#         save_to_db(chiller, y_col, modelos[melhor_modelo], scaler, melhor_modelo)

#     joblib.dump(scaler, f'{modelPath}/scaler.pkl')

#     if melhor_modelo == 'Neural Network':
#         model_nn.save(f'{modelPath}/model.h5')
#         params = {'y_mean': y.mean(), 'y_std': y.std()}
#         joblib.dump(params, f'{modelPath}/params_y_normalization.pkl')
#     else:
#         joblib.dump(modelos[melhor_modelo], f'{modelPath}/model.pkl')


#     return  y_col, df_resultados, melhor_modelo

def Prever(siteID, siteName, df, chiller, X, y_col):    
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping
    import sqlite3
    import pickle
    from datetime import datetime
    import joblib
    import os

    modelPath = f'models/{siteID}_{siteName}/{chiller}/{y_col}'
    os.makedirs(modelPath, exist_ok=True)

    def save_to_db(chiller, y_col, modelPath, model, scaler, model_name, r2, mae, mse):
        """
        Função para salvar o modelo, scaler e métricas no banco de dados SQLite.
        """
        conn = sqlite3.connect("models.db")
        cursor = conn.cursor()

        # Criar tabela, se ainda não existir
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siteID INTEGER NOT NULL,
            siteName TEXT NOT NULL,
            chiller TEXT NOT NULL,
            y_col TEXT NOT NULL,
            modelPath TEXT NOT NULL,
            model_name TEXT NOT NULL,
            model_data BLOB NOT NULL,
            scaler_data BLOB NOT NULL,
            r2 REAL NOT NULL,
            mae REAL NOT NULL,
            mse REAL NOT NULL,
            created_at TEXT NOT NULL
        );
        """)

        # Serializar modelo e scaler
        model_data = pickle.dumps(model)
        scaler_data = pickle.dumps(scaler)

        # Inserir no banco de dados
        query = """
        INSERT INTO Models (siteID, siteName, chiller, y_col, modelPath, model_name, model_data, scaler_data, r2, mae, mse, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(query, (siteID, siteName, chiller, y_col, modelPath, model_name, model_data, scaler_data, r2, mae, mse, datetime.now()))
        conn.commit()

        cursor.close()
        conn.close()

    # Separando as features (X) e o target (y)
    X = df[X]
    y = df[y_col]

    # Dividindo o dataset em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    # Normalizando os dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Modelos a serem avaliados
    modelos = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Extra Trees': ExtraTreesRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
    }

    # Avaliação dos modelos
    resultados = []
    for nome, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        resultados.append([nome, mse, r2, mae])
        print(f'{nome}: MSE={mse:.4f}, R²={r2:.4f}, MAE={mae:.4f}')

    # Avaliação da Rede Neural
    model_nn = Sequential([
        Dense(64, input_dim=X_train.shape[1], activation='relu'),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='linear')
    ])
    model_nn.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model_nn.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=32, callbacks=[early_stopping], verbose=0)
    y_pred_nn = model_nn.predict(X_test).flatten()

    # Métricas da rede neural
    mse_nn = mean_squared_error(y_test, y_pred_nn)
    r2_nn = r2_score(y_test, y_pred_nn)
    mae_nn = mean_absolute_error(y_test, y_pred_nn)
    resultados.append(['Neural Network', mse_nn, r2_nn, mae_nn])
    print(f'Neural Network: MSE={mse_nn:.4f}, R²={r2_nn:.4f}, MAE={mae_nn:.4f}')

    # Criação da tabela de resultados com 4 casas decimais
    df_resultados = pd.DataFrame(resultados, columns=['Modelo', 'MSE', 'R²', 'MAE'])
    df_resultados[['MSE', 'R²', 'MAE']] = df_resultados[['MSE', 'R²', 'MAE']].applymap(lambda x: f"{x:.4f}")

    # Eleger o melhor modelo com base no R²
    indice_melhor_modelo = df_resultados['R²'].astype(float).idxmax()
    melhor_modelo = df_resultados.loc[indice_melhor_modelo, 'Modelo']
    print(f'Melhor modelo: {melhor_modelo}')

    # Salvar o melhor modelo e o scaler no banco
    if melhor_modelo == 'Neural Network':
        save_to_db(chiller, y_col, modelPath, model_nn, scaler, 'Neural Network', r2_nn, mae_nn, mse_nn)
    else:
        best_model = modelos[melhor_modelo]
        y_pred_best = best_model.predict(X_test)
        mse_best = mean_squared_error(y_test, y_pred_best)
        r2_best = r2_score(y_test, y_pred_best)
        mae_best = mean_absolute_error(y_test, y_pred_best)
        save_to_db(chiller, y_col, modelPath, best_model, scaler, melhor_modelo, r2_best, mae_best, mse_best)

    joblib.dump(scaler, f'{modelPath}/scaler.pkl')

    if melhor_modelo == 'Neural Network':
        model_nn.save(f'{modelPath}/model.h5')
        params = {'y_mean': y.mean(), 'y_std': y.std()}
        joblib.dump(params, f'{modelPath}/params_y_normalization.pkl')
    else:
        joblib.dump(modelos[melhor_modelo], f'{modelPath}/model.pkl')

    return y_col, df_resultados, melhor_modelo
