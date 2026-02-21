# =================================================================
# GESTIÓN DE EXPERIMENTOS CON MLFLOW
# =================================================================

# 1. Importamos el módulo de MLflow para interactuar con el servidor de rastreo
import mlflow

# 2. Creamos un nuevo experimento llamado "Unicorn Model"
# Esto genera un identificador único y un espacio en el Metadata Store para los resultados 
mlflow.create_experiment("Unicorn Model")

# 3. Establecemos etiquetas (tags) para añadir metadatos descriptivos al experimento
# Las etiquetas como "version" son vitales para la auditoría y el archivado de modelos [cite: 5, 45]
mlflow.set_experiment_tag("version", "1.0")

# 4. Definimos "Unicorn Model" como el experimento activo
# Esto asegura que todas las métricas, parámetros y artefactos futuros se registren aquí [cite: 5]
mlflow.set_experiment("Unicorn Model")

# Autodocumentación: 
# Ahora MLflow sabe que cualquier ejecución (run) iniciada a continuación 
# pertenece a la versión 1.0 del proyecto Unicorn.
