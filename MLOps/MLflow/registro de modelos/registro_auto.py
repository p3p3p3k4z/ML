# =================================================================
# REGISTRO AUTOMÁTICO Y BÚSQUEDA EN EL REGISTRO
# =================================================================

# 1. Registro del modelo con el Sabor (Flavor) de Scikit-Learn
# artifact_path="model": Define la carpeta dentro de MLflow donde se guardan los archivos.
# registered_model_name="Insurance": Crea o añade una versión al catálogo 'Insurance'.
mlflow.sklearn.log_model(lr, "model", registered_model_name="Insurance")

# 2. Definición de la cadena de filtro
# Usamos sintaxis SQL-like para buscar coincidencias exactas por nombre.
insurance_filter_string = "name = 'Insurance'"

# 3. Consulta al Model Registry vía MlflowClient
# El cliente nos permite inspeccionar el estado del registro de forma global.
print(client.search_registered_models(filter_string=insurance_filter_string))
