# =================================================================
# REGISTRO Y CARGA DE MODELOS DESDE MLFLOW TRACKING
# =================================================================

# 1. Registramos el modelo entrenado en MLflow Tracking.
# Usamos el "sabor" (flavor) sklearn y definimos la ruta del artefacto como "lr_tracking".
# Esto almacena el binario del modelo y sus metadatos en el servidor.
mlflow.sklearn.log_model(lr_model, "lr_tracking")

# 2. Obtenemos el objeto de la última ejecución (run) activa.
# Esto nos permite acceder a los metadatos de la carrera que acabamos de realizar.
run = mlflow.last_active_run()

# 3. Extraemos el identificador único de la ejecución (run_id).
# El run_id es la clave necesaria para localizar artefactos específicos en el sistema.
run_id = run.info.run_id

# 4. Cargamos el modelo directamente desde MLflow Tracking.
# Utilizamos el URI con el formato "runs:/<run_id>/<ruta_artefacto>".
# Este método garantiza que cargamos exactamente el modelo generado en esa ejecución.
model = mlflow.sklearn.load_model(f"runs:/{run_id}/lr_tracking")

# Autodocumentación:
# Este flujo permite que el modelo sea persistente y accesible para otros 
# pasos de evaluación o despliegue sin depender de archivos locales.
