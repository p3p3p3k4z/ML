# =================================================================
# DEFINICIÓN Y EJECUCIÓN DE LA TRANSFORMACIÓN (ELT)
# =================================================================

# Completamos la función transform()
def transform(source_table, target_table):
  # El método .execute() es el estándar para enviar comandos SQL
  # directamente al motor del Data Warehouse.
  data_warehouse.execute(f"""
  CREATE TABLE {target_table} AS
      SELECT
          CONCAT("Product ID: ", product_id),
          quantity * price
      FROM {source_table};
  """)

# 1. Extracción
extracted_data = extract(file_name="raw_sales_data.csv")

# 2. Carga (Load) de datos crudos
load(data_frame=extracted_data, table_name="raw_sales_data")

# 3. Transformación: Poblamos la tabla total_sales desde raw_sales_data
transform(source_table="raw_sales_data", target_table="total_sales")
