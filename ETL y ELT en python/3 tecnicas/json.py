import pandas as pd
import json
import os
import logging

# Configuración de supervisión
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# =================================================================
# MÓDULO DE PROCESAMIENTO JSON
# =================================================================

def extract_json_native(file_path):
    """
    Extracción Nativa (Lightweight).
    Ideal para archivos de configuración o cuando la memoria es limitada.
    """
    logging.info(f"Cargando JSON nativo desde: {file_path}")
    with open(file_path, "r") as f:
        # json.load lee el objeto de archivo y devuelve un diccionario/lista
        return json.load(f)

def extract_json_pandas(file_path, orientation="records"):
    """
    Extracción con Pandas (Analítica).
    Convierte JSON directamente en tabla para transformaciones masivas.
    """
    logging.info(f"Ingiriendo JSON con Pandas (Orientación: {orientation})")
    # read_json es excelente cuando el JSON ya tiene estructura tabular
    return pd.read_json(file_path, orient=orientation)

def transform_json_data(df):
    """
    Transformación: Limpieza y validación.
    """
    logging.info("Transformando datos JSON...")
    # Ejemplo: Eliminar filas con datos nulos en columnas críticas
    clean_df = df.dropna().copy()
    
    # Aquí podrías añadir lógica de 'flattening' si el JSON fuera anidado
    return clean_df

def load_json_to_file(df, output_path, orientation="records"):
    """
    Carga: Persistencia en formato JSON.
    """
    logging.info(f"Persistiendo resultados en: {output_path}")
    # to_json permite guardar el DataFrame de vuelta a texto plano
    df.to_json(output_path, orient=orientation, indent=4)
    
    if os.path.exists(output_path):
        logging.info("✅ Archivo JSON guardado exitosamente.")

# =================================================================
# EJECUCIÓN DEL FLUJO
# =================================================================

if __name__ == "__main__":
    # 1. Ejemplo de extracción nativa (útil para inspección rápida)
    # raw_data = extract_json_native("testing_scores.json")
    
    try:
        # 2. Ingesta con Pandas (usando los conceptos de tus ejercicios)
        # Probamos con orientación 'records' que es el estándar de APIs
        df_scores = extract_json_pandas("testing_scores.json", orientation="records")
        
        # 3. Transformación
        df_cleaned = transform_json_data(df_scores)
        
        # 4. Carga final
        load_json_to_file(df_cleaned, "final_scores_report.json")
        
        print("\n--- VISTA PREVIA DE LOS DATOS ---")
        print(df_cleaned.head())

    except ValueError as e:
        logging.error(f"Error de formato JSON: {e}. Verifica la orientación (records vs index).")
    except FileNotFoundError:
        logging.error("No se encontró el archivo .json en la ruta especificada.")
