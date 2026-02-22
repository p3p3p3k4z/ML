# =================================================================
# EJECUCIÓN DE PIPELINE ELT: PRIORIZANDO LA CARGA
# =================================================================

# 1. Extraemos los datos del archivo origen (Extract)
raw_data = extract(file_name="raw_data.csv")

# 2. Cargamos los datos CRUDOS directamente al almacén (Load)
# A diferencia del ETL, aquí no hemos limpiado nada todavía.
load(data_frame=raw_data, table_name="raw_data")

# 3. Ejecutamos la transformación DENTRO del almacén (Transform)
# Generalmente, esto dispara una consulta SQL interna en el destino.
transform(
  source_table="raw_data", 
  target_table="cleaned_data"
)

# Autodocumentación:
# En este escenario, Python funciona como un orquestador que "mueve" 
# los datos y "ordena" la ejecución, pero no consume CPU transformando.
