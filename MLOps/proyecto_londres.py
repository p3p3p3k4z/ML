import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

# 1. Carga y limpieza de datos
weather = pd.read_csv("london_weather.csv")

# Eliminamos registros donde el objetivo (mean_temp) sea nulo
weather = weather.dropna(subset=['mean_temp'])

# Selección de características (features) y objetivo (target)
features = ['cloud_cover', 'sunshine', 'global_radiation', 'max_temp', 'min_temp', 'precipitation', 'pressure', 'snow_depth']
target = 'mean_temp'

X = weather[features]
y = weather[target]

# 2. Preprocesamiento (Imputación y Escalado)
# Tratamos los nulos en las características y normalizamos los datos
imputer = SimpleImputer(strategy='mean')
scaler = StandardScaler()

X_imputed = imputer.fit_transform(X)
X_scaled = scaler.fit_transform(X_imputed)

# División entrenamiento/prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 3. Configuración del Experimento en MLflow
mlflow.set_experiment("London_Temperature_Prediction")

# Definimos los modelos a experimentar
# Nota: Random Forest suele ser el más preciso para este dataset
experiment_configs = [
    {"name": "Linear_Regression", "model": LinearRegression(), "params": {}},
    {"name": "Decision_Tree", "model": DecisionTreeRegressor(max_depth=5), "params": {"max_depth": 5}},
    {"name": "Random_Forest", "model": RandomForestRegressor(n_estimators=100, max_depth=10), "params": {"n_estimators": 100, "max_depth": 10}}
]

# 4. Ciclo de Experimentación
for config in experiment_configs:
    with mlflow.start_run(run_name=config["name"]):
        # Entrenamiento
        model = config["model"]
        model.fit(X_train, y_train)
        
        # Predicción y cálculo de la métrica
        predictions = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        
        # --- Registro de Datos (Logging) ---
        # Registramos hiperparámetros si existen
        if config["params"]:
            mlflow.log_params(config["params"])
        
        # Registramos la métrica obligatoria
        mlflow.log_metric("rmse", rmse)
        
        # Registramos el modelo (Sabor sklearn)
        mlflow.sklearn.log_model(model, "model")
        
        print(f"✅ Ejecución: {config['name']} | RMSE: {rmse:.4f}")

# 5. Búsqueda y almacenamiento de resultados
# Recuperamos todas las ejecuciones para el análisis final
experiment_results = mlflow.search_runs()

# Visualización rápida del mejor resultado
print("\n--- Resultados de los Experimentos ---")
print(experiment_results[['run_id', 'params.max_depth', 'metrics.rmse']].sort_values(by='metrics.rmse'))
