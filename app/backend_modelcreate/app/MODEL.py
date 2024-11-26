def Prever(df, chiller, X, y_col):    
    import joblib
    import os
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')  # Define um backend que não depende de uma interface gráfica
    import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, Lasso
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, AdaBoostRegressor
    from sklearn.svm import SVR
    import xgboost as xgb
    import lightgbm as lgb
    from catboost import CatBoostRegressor
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping
    from sklearn.neighbors import KNeighborsRegressor

    # Criação do diretório para salvar o modelo e scaler
    os.makedirs(f'ModelsDeploy/{chiller}/{y_col}', exist_ok=True)

    # Separando as features (X) e o target (y)
    X = df[X]
    y = df[y_col]

    # Dividindo o dataset em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    assert X_train.shape[0] > 0, "O conjunto de treinamento está vazio."
    assert not X_train.isnull().any().any(), "Existem valores ausentes nas features."

    # Normalizando os dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Modelos a serem avaliados
    modelos = {
        'Linear': LinearRegression(),
        'Ridge': Ridge(alpha=1.0),
        'Lasso': Lasso(alpha=1.0),
        'ElasticNet': ElasticNet(alpha=1.0, l1_ratio=0.5),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Extra Trees': ExtraTreesRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
        'AdaBoost': AdaBoostRegressor(n_estimators=100, random_state=42),
        'KNeighbors': KNeighborsRegressor(n_neighbors=5),
        'SVR': SVR(kernel='rbf'),
        'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42),
        'LightGBM': lgb.LGBMRegressor(n_estimators=100, random_state=42),
        'CatBoost': CatBoostRegressor(n_estimators=100, random_state=42, verbose=0)
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

    # Salvar o melhor modelo e o scaler
    joblib.dump(scaler, f'ModelsDeploy/{chiller}/{y_col}/scaler.pkl')
    
    if melhor_modelo == 'Neural Network':
        model_nn.save(f'ModelsDeploy/{chiller}/{y_col}/model.h5')
        params = {'y_mean': y.mean(), 'y_std': y.std()}
        joblib.dump(params, f'ModelsDeploy/{chiller}/{y_col}/params_y_normalization.pkl')
    else:
        joblib.dump(modelos[melhor_modelo], f'ModelsDeploy/{chiller}/{y_col}/model.pkl')


    return y_col, df_resultados, melhor_modelo 

