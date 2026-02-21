# =================================================================
# REGISTRO DE MODELOS EXISTENTES EN EL MODEL REGISTRY
# =================================================================

# 1. Registramos el primer modelo (versión 2022).
# Al estar en un directorio local ("model_2022"), MLflow lo sube al registro 
# bajo el nombre centralizado "Insurance". 
# Esto permite que un modelo que antes estaba "suelto" ahora tenga gobernanza.
mlflow.register_model("model_2022", "Insurance")

# 2. Registramos el segundo modelo (versión 2023).
# Este ya existe en el Tracking Server, por lo que usamos su dirección URI 
# con el formato f"runs:/{run_id}/[ruta_del_artefacto]".
# Lo registramos bajo el mismo nombre "Insurance" para crear la versión 2.
mlflow.register_model(f"runs:/{run_id}/model_2023", "Insurance")

# Autodocumentación:
# Al registrar ambos modelos bajo el nombre "Insurance", el Model Registry 
# les asigna automáticamente versiones (v1 y v2). 
# Esto es vital para la reproducibilidad y para gestionar las transiciones 
# de etapa (Staging, Production, Archived).
