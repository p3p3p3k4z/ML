# =================================================================
# REGISTRO Y EVALUACIÓN AUTOMÁTICA CON MLFLOW
# =================================================================

# Preparación de los datos de evaluación (Contexto del ejercicio)
eval_data = X_test
eval_data["sex"] = y_test

# 1. Registramos el modelo 'lr_class' usando el Sabor (Flavor) incorporado de Scikit-Learn.
# Esto empaqueta el modelo de forma estándar para su posterior carga y evaluación.
mlflow.sklearn.log_model(lr_class, "model")

# 2. Obtenemos el identificador único de la ejecución activa (run_id).
# El run_id nos permite localizar el artefacto del modelo recién guardado en el servidor.
run = mlflow.last_active_run()
run_id = run.info.run_id

# 3. Evaluamos el modelo registrado utilizando la función mlflow.evaluate().
# - f"runs:/{run_id}/model": Indicamos la ubicación del modelo mediante su URI.
# - data: Pasamos el DataFrame 'eval_data' que contiene las características y el target.
# - targets: Especificamos la columna "sex" como el objetivo a predecir.
# - model_type: Definimos que es un "classifier" para que MLflow genere métricas de clasificación (Accuracy, Precision, etc.).
mlflow.evaluate(f"runs:/{run_id}/model", 
        data=eval_data, 
        targets="sex",
        model_type="classifier"
)

# Autodocumentación:
# Al ejecutar mlflow.evaluate(), MLflow no solo calcula las métricas, sino que 
# las registra automáticamente en el servidor de Seguimiento (Tracking), 
# permitiendo comparar este modelo con otros en la fase de Evaluación.
