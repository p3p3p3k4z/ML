# =================================================================
# CONSTRUCCIÓN Y EJECUCIÓN DE CANALIZACIÓN ETL
# =================================================================

def load(data_frame, file_name):
  # Escribimos el DataFrame limpio en un archivo .csv
  # El método to_csv es el estándar en pandas para persistencia en archivos
  data_frame.to_csv(file_name, index=False)
  print(f"Successfully loaded data to {file_name}")

# 1. Extracción (Fase inicial)
extracted_data = extract(file_name="raw_data.csv")

# 2. Transformación (Limpieza y preparación)
# Usamos la función transform() sobre los datos extraídos
transformed_data = transform(data_frame=extracted_data)

# 3. Carga (Persistencia final)
# Guardamos el resultado en el archivo destino
load(data_frame=transformed_data, file_name="transformed_data.csv")
