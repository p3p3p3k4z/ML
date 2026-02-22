import pandas as pd

# 1. Leemos los datos de ventas desde el archivo Parquet
# El motor 'fastparquet' es excelente para optimizar el rendimiento de I/O
sales_data = pd.read_parquet("sales_data.parquet", engine="fastparquet")

# 2. Comprobamos los tipos de datos de las columnas
# A diferencia de los CSV, Parquet conserva el esquema (schema) original
print(sales_data.dtypes)

# 3. Mostramos la forma (filas, columnas) y el encabezado
# Útil para verificar rápidamente que la ingesta fue correcta
print(sales_data.shape)
print(sales_data.head())
