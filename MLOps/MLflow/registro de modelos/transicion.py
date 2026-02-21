# =================================================================
# GESTIÓN INTEGRAL DEL CICLO DE VIDA: PROYECTO "INSURANCE"
# =================================================================

from mlflow import MlflowClient

# Inicializamos el cliente para interactuar con el Model Registry
client = MlflowClient()
nombre_modelo = "Insurance"

# --- 1. PROMOCIÓN A PRODUCCIÓN (VERSIÓN MÁS ESTABLE) ---
# La versión 2 ha pasado todas las validaciones y es designada como 
# la versión oficial para servir predicciones a los usuarios finales.
client.transition_model_version_stage(
    name=nombre_modelo, 
    version=2,
    stage="Production"
)
print(f"Retroalimentación: Versión 2 de '{nombre_modelo}' movida a PRODUCTION.")

# --- 2. TRANSICIÓN A STAGING (FASE DE PRUEBAS) ---
# La versión 3 es la más reciente. Se mueve a 'Staging' para que el 
# equipo de QA realice pruebas de integración y validación de métricas.
client.transition_model_version_stage(
    name=nombre_modelo, 
    version=3,
    stage="Staging"
)
print(f"Retroalimentación: Versión 3 de '{nombre_modelo}' movida a STAGING.")

# --- 3. ARCHIVADO DE VERSIONES OBSOLETAS ---
# La versión 1 ya no es necesaria o ha sido superada. Se mueve a 'Archived' 
# para retirarla del flujo activo pero manteniendo su historial para auditorías.
client.transition_model_version_stage(
    name=nombre_modelo, 
    version=1,
    stage="Archived"
)
print(f"Retroalimentación: Versión 1 de '{nombre_modelo}' movida a ARCHIVED.")

# Autodocumentación:
# Al finalizar este script, el registro tiene una estructura jerárquica clara:
# - Production: Versión 2 (Servicio activo)
# - Staging: Versión 3 (En evaluación)
# - Archived: Versión 1 (Histórico)
