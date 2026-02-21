# =================================================================
# REGISTRO DE MÉTRICAS, PARÁMETROS Y ARTEFACTOS EN MLFLOW
# =================================================================

# 1. Registramos la métrica de rendimiento.
# Las métricas son valores numéricos que pueden cambiar (ej. R2, pérdida, precisión).
# Aquí guardamos el valor de la variable r2_score bajo el nombre "r2_score".
mlflow.log_metric("r2_score", r2_score)

# 2. Registramos el parámetro de configuración del modelo.
# Los parámetros son constantes elegidas antes del entrenamiento (ej. hiperparámetros).
# Guardamos "n_jobs" con el valor 1 para saber cómo se configuró el algoritmo.
mlflow.log_param("n_jobs", 1)

# 3. Registramos el código de entrenamiento como un artefacto.
# Los artefactos son archivos externos (modelos, scripts, imágenes) asociados a la ejecución.
# Guardamos "train.py" para garantizar que siempre sepamos qué código generó este modelo.
mlflow.log_artifact("train.py")

# Autodocumentación:
# Al registrar estos tres elementos, has creado un registro inmutable en el Tracking Server.
# Esto permite que, meses después, cualquier miembro del equipo pueda entender 
# el rendimiento (métrica), la configuración (parámetro) y la lógica (artefacto) de este modelo.
