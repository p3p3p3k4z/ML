# =================================================================
# EJECUCIÓN DEL PROYECTO CON PARÁMETROS ESPECÍFICOS (CORREGIDO)
# =================================================================

import mlflow

# Llamamos a la función run del módulo projects
# Esta función es la que "dispara" el entrenamiento automatizado.
mlflow.projects.run(
    uri='./',
    entry_point='main',
    experiment_name='Insurance',
    env_manager='local',
    # Usamos las claves exactas definidas en el archivo MLproject del ejercicio:
    # 'n_jobs_param' y 'fit_intercept_param'.
    parameters={
        'n_jobs_param': 2, 
        'fit_intercept_param': False
    }
)

# Autodocumentación:
# Al ejecutar esto, MLflow busca en el MLproject el entry_point 'main'
# e inyecta estos valores en el comando: 
# "python3.9 train_model.py 2 False"
