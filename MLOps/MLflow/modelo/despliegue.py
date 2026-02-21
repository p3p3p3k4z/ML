# =================================================================
# DESPLIEGUE DE MODELO PERSONALIZADO CON MLFLOW PYFUNC
# =================================================================

# 1. Registramos el modelo personalizado utilizando el sabor pyfunc.
# - artifact_path: Nombre de la carpeta donde se guardará el modelo.
# - python_model: Instancia de nuestra clase personalizada CustomPredict.
# - artifacts: Diccionario que vincula nombres lógicos con rutas de archivos físicos (el modelo de sklearn).
mlflow.pyfunc.log_model(
    artifact_path="lr_pyfunc", 
    # Establecemos que el modelo use la lógica definida en CustomPredict()
    python_model=CustomPredict(), 
    artifacts={"lr_model": "lr_model"}
)

# Recuperamos los metadatos de la última ejecución para obtener el run_id
run = mlflow.last_active_run()
run_id = run.info.run_id

# 2. Cargamos el modelo en formato python_function.
# Al cargarlo con pyfunc.load_model, MLflow reconstruye la clase CustomPredict 
# y ejecuta su método load_context() automáticamente.
loaded_model = mlflow.pyfunc.load_model(f"runs:/{run_id}/lr_pyfunc")

# Autodocumentación:
# A partir de ahora, al llamar a loaded_model.predict(), el sistema ejecutará 
# la lógica personalizada que transforma las predicciones numéricas en 
# etiquetas de texto ("female"/"male"), garantizando un despliegue transparente.
