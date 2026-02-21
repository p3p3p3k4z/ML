# =================================================================
# EJECUCIÓN PROGRAMÁTICA DE PROYECTOS (MLFLOW PROJECTS)
# =================================================================

import mlflow

# 1. Llamamos a la función run() del módulo mlflow.projects.
# Esta función permite disparar la ejecución de un MLproject desde Python.
mlflow.projects.run(
    # 2. Establecemos el URI como el directorio de trabajo actual ('./').
    # Aquí es donde MLflow buscará el archivo 'MLproject' para configurarse.
    uri='./',
    # 3. Definimos el punto de entrada (entry_point) como 'main'.
    # Esto ejecutará el comando asociado en el archivo MLproject.
    entry_point='main',
    # 4. Asignamos el nombre del experimento como 'Insurance'.
    # Todos los parámetros, métricas y modelos se guardarán bajo este nombre.
    experiment_name='Insurance',
    # Usamos el administrador de entorno local y ejecución síncrona para el ejercicio.
    env_manager="local",
    synchronous=True,
)

# Autodocumentación:
# Al usar mlflow.projects.run(), MLflow gestiona automáticamente el ciclo de vida
# de la ejecución, asegurando que el experimento 'Insurance' sea el destino
# correcto para toda la trazabilidad generada por el script 'main'.
