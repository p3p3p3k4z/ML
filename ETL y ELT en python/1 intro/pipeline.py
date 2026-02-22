import pandas as pd
import os

# =================================================================
# PIPELINE ETL: GESTIÓN DE DATOS INDUSTRIALES / ESTUDIANTILES
# Propósito: Extraer métricas crudas, filtrar información crítica 
#            y asegurar la persistencia para análisis posterior.
# =================================================================

def extract(file_name):
    """
    PROPÓSITO: Punto de entrada del pipeline.
    POR QUÉ: Centralizar la lectura permite manejar errores de I/O 
    (Input/Output) en un solo lugar. Si el origen cambia de un CSV 
    a una base de datos SQL, solo modificamos esta función.
    """
    print(f"🔍 [EXTRACT] Accediendo a la fuente: {file_name}")
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"❌ Error: El archivo {file_name} no existe.")
        return None

def transform(data_frame):
    """
    PROPÓSITO: Refinamiento y lógica de negocio.
    POR QUÉ: 
    1. Optimización: Reducimos el uso de memoria RAM al descartar 
       columnas innecesarias.
    2. Seguridad: Evitamos que datos sensibles viajen al destino final.
    3. Rendimiento: El filtrado con .loc es vectorizado y eficiente.
    """
    print("🛠️ [TRANSFORM] Filtrando columnas críticas...")
    # Seleccionamos solo industry_name y number_of_firms
    # Usamos .loc para asegurar que trabajamos sobre la estructura correcta
    columns_to_keep = ["industry_name", "number_of_firms"]
    return data_frame.loc[:, columns_to_keep]

def load(data_frame, file_name):
    """
    PROPÓSITO: Persistencia de estado (Output).
    POR QUÉ: El valor del ETL reside en que el resultado sea consultable. 
    Usamos index=False para evitar 'polución de datos' (columnas de 
    índices innecesarias en el CSV de salida).
    """
    print(f"💾 [LOAD] Guardando datos transformados en: {file_name}")
    data_frame.to_csv(file_name, index=False)
    print("✅ Carga finalizada con éxito.")

# =================================================================
# ORQUESTACIÓN DEL PROCESO
# =================================================================

def run_etl_pipeline():
    # 1. Fase de Extracción
    raw_data_path = "raw_data.csv"
    extracted_data = extract(raw_data_path)
    
    if extracted_data is not None:
        # 2. Fase de Transformación
        transformed_data = transform(extracted_data)
        
        # 3. Fase de Carga
        output_path = "number_of_firms.csv"
        load(transformed_data, output_path)
    else:
        print("🛑 Pipeline detenido: No se pudo obtener la fuente de datos.")

if __name__ == "__main__":
    run_etl_pipeline()
