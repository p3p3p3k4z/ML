import sqlalchemy
import pandas as pd

# 1. Creamos el motor de conexión (engine)
# El URI sigue el patrón: dialecto+driver://usuario:password@host:puerto/nombre_db
db_engine = sqlalchemy.create_engine("postgresql+psycopg2://repl:password@localhost:5432/sales")

# 2. Consultamos la tabla 'sales' usando pandas
# read_sql es el puente perfecto: toma una consulta o nombre de tabla y el motor
raw_sales_data = pd.read_sql("sales", db_engine)

# 3. Mostramos los resultados
print(raw_sales_data)

def extract():
    connection_uri = "postgresql+psycopg2://repl:password@localhost:5432/sales"
    db_engine = sqlalchemy.create_engine(connection_uri)
    raw_data = pd.read_sql("SELECT * FROM sales WHERE quantity_ordered = 1", db_engine)
    
    # 1. Imprimimos las primeras filas (Sanity Check)
    # Esto nos permite verificar visualmente que el esquema es el esperado
    print(raw_data.head())
    
    # 2. Devolvemos el DataFrame extraído
    return raw_data
    
# 3. Ejecutamos la función y guardamos el resultado
# Aquí es donde "disparamos" la conexión a la base de datos
raw_sales_data = extract()
