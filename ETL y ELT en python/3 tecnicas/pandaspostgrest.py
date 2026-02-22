import pandas as pd
import sqlalchemy
import logging

# 1. CONFIGURACIÓN DE LOGGING (Esencial para SysAdmins)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# 2. DEFINICIÓN DE FUNCIONES DEL PIPELINE

def extract(file_path):
    """Extrae datos de una fuente JSON."""
    logging.info(f"Extrayendo datos de {file_path}...")
    # Usamos orient='records' asumiendo el estándar de APIs
    return pd.read_json(file_path, orient='records')

def transform(raw_data):
    """Limpia, imputa valores y agrupa los datos."""
    logging.info("Iniciando transformación y limpieza...")
    
    # A. Imputación de valores faltantes (Media aritmética)
    # $\bar{x} = \frac{1}{n} \sum x_i$
    raw_data.fillna(
        value={
            "math_score": raw_data["math_score"].mean(),
            "reading_score": raw_data["reading_score"].mean(),
            "writing_score": raw_data["writing_score"].mean()
        }, inplace=True
    )
    
    # B. Agrupamiento y Modelado
    # Agrupamos por ciudad para obtener promedios regionales
    grouped_data = raw_data.loc[:, ["city", "math_score", "reading_score", "writing_score"]]
    return grouped_data.groupby(by=["city"]).mean()

def load(clean_data, db_engine):
    """Persiste los datos en la base de datos PostgreSQL."""
    logging.info("Cargando datos en la tabla 'scores_by_city'...")
    clean_data.to_sql(
        name="scores_by_city",
        con=db_engine,
        if_exists="replace", # Sobrescribir para mantener la idempotencia
        index=True,          # Mantener el nombre de la ciudad como índice
        index_label="city"
    )

def validate(db_engine):
    """Verifica que los datos se hayan guardado correctamente (Prueba de Humo)."""
    logging.info("Validando persistencia de datos...")
    # Cerramos el ciclo leyendo directamente de la DB
    query = "SELECT * FROM scores_by_city LIMIT 5"
    df_validation = pd.read_sql(query, con=db_engine)
    
    if not df_validation.empty:
        logging.info("✅ Validación exitosa: Los datos están disponibles en Postgres.")
        return df_validation
    else:
        logging.error("❌ Fallo de validación: La tabla está vacía.")
        return None

# 3. EJECUCIÓN DEL PROCESO UNIFICADO

# Cadena de conexión (Protocolo + Driver + Credenciales)
# 
conn_string = "postgresql+psycopg2://repl:password@localhost:5432/schools"
db_engine = sqlalchemy.create_engine(conn_string)

try:
    # Ejecutar Pipeline
    raw_data = extract("testing_scores.json")
    clean_data = transform(raw_data)
    load(clean_data, db_engine)
    
    # Paso final: Validación
    # 
    results = validate(db_engine)
    print("\n--- RESULTADOS CARGADOS Y VALIDADOS ---")
    print(results)

except Exception as e:
    logging.critical(f"Error crítico en el pipeline: {e}")
