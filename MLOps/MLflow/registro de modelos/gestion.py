# =================================================================
# GESTIÓN DEL MODEL REGISTRY CON MLFLOW CLIENT
# =================================================================

# 1. Importamos la clase MlflowClient del módulo mlflow.
# Esta clase proporciona la API de bajo nivel para interactuar con el 
# Tracking Server y el Model Registry.
from mlflow import MlflowClient

# 2. Creamos una instancia de la clase MlflowClient.
# El objeto 'client' nos permite realizar operaciones administrativas, 
# como crear modelos, cambiar sus etapas o eliminar versiones.
client = MlflowClient()

# 3. Creamos un nuevo modelo registrado llamado "Insurance".
# Este paso crea una ubicación de almacenamiento centralizada en el Registro.
# A partir de aquí, podremos añadir diferentes versiones (v1, v2...) de este modelo.
client.create_registered_model("Insurance")

# Autodocumentación:
# El Model Registry es crucial para la colaboración, ya que permite que 
# diferentes equipos carguen y desplieguen modelos de forma estandarizada, 
# gestionando su transición entre etapas como 'Staging' o 'Production'.
