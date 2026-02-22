# =================================================================
# EJECUCIÓN DE PIPELINE ETL: FLUJO DE TRABAJO MODULAR
# =================================================================

# 1. Extraemos los datos del archivo crudo (Raw Data)
extracted_data = extract(file_name="raw_data.csv")

# 2. Transformamos el DataFrame extraído 
# (Aquí es donde se limpia y prepara la información)
transformed_data = transform(data_frame=extracted_data)

# 3. Cargamos los datos transformados en la tabla de destino
load(data_frame=transformed_data, target_table="cleaned_data")

# Autodocumentación:
# Al separar estas fases, puedes monitorear el tiempo de ejecución de cada una
# y depurar fallos de forma aislada en tus servidores de producción.
