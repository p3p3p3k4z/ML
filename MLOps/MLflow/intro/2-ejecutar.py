# =================================================================
# INICIO DE UNA EJECUCIÓN (RUN) EN MLFLOW
# =================================================================

# 1. Configuramos el experimento activo. 
# Esto le indica a MLflow que todas las ejecuciones iniciadas a partir de ahora
# deben agruparse bajo el contenedor "Unicorn Sklearn Experiment".
mlflow.set_experiment("Unicorn Sklearn Experiment")

# 2. Iniciamos una nueva ejecución (run).
# Al activar una ejecución, habilitamos el rastreo de métricas, parámetros 
# y artefactos para esta sesión específica de entrenamiento.
mlflow.start_run()

# Autodocumentación:
# A partir de este punto, el "Metadata Store" está listo para recibir datos.
# Recuerda que, por buena práctica, cada 'run' debe cerrarse o usarse 
# dentro de un bloque 'with' en scripts reales para liberar recursos.
