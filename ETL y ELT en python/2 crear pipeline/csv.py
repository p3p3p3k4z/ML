import pandas as pd
import os
from datetime import datetime

# =================================================================
# PIPELINE DE DATOS INTEGRADO (FILE-BASED ETL)
# Propósito: Procesar registros de ventas desde fuentes heterogéneas
#            asegurando integridad de tipos y persistencia personalizada.
# =================================================================

# --- CONFIGURACIÓN DE RUTAS ---
INPUT_FILE = "sales_data.parquet"  # Fuente original (Binario/Columnar)
OUTPUT_FILE = "transformed_sales_report.csv" # Destino (Texto Plano/Intercambio)

def extract(file_path):
    """
    FASE 1: EXTRACCIÓN
    POR QUÉ: Manejar diferentes formatos permite al pipeline ser flexible.
    """
    print(f"📦 [EXTRACT] Iniciando ingesta desde: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe en el volumen.")

    # Lógica de selección de motor según extensión
    if file_path.endswith('.parquet'):
        return pd.read_parquet(file_path, engine="fastparquet")
    else:
        return pd.read_csv(file_path)

def transform(df):
    """
    FASE 2: TRANSFORMACIÓN Y LIMPIEZA
    POR QUÉ: Aquí reducimos la carga computacional y normalizamos datos.
    """
    print("🛠️ [TRANSFORM] Aplicando lógica de negocio y tipado...")

    # 1. Normalización de Tipos (Datetime Casting)
    # Vital para que el sistema entienda el orden cronológico
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%y %H:%M")

    # 2. Filtrado Lógico (Poda de datos)
    # Solo artículos económicos (< 25$) y pedidos unitarios (== 1)
    # Esto reduce el tamaño del dataset en RAM
    query_condition = (df["Price Each"] < 25) & (df["Quantity Ordered"] == 1)
    clean_data = df.loc[query_condition, :].copy()

    # 3. Proyección (Selección de columnas críticas)
    cols = ["Order ID", "Product", "Price Each", "Order Date", "Quantity Ordered"]
    return clean_data.loc[:, cols]

def load(df, target_path):
    """
    FASE 3: CARGA Y PERSISTENCIA PERSONALIZADA
    POR QUÉ: Formatear la salida facilita la ingesta en procesos posteriores.
    """
    print(f"💾 [LOAD] Persistiendo datos en: {target_path}")
    
    # Personalización: Sin cabecera (para logs/append), sin índice (limpieza)
    # y usando separador de tubería (|) para evitar conflictos con comas.
    df.to_csv(target_path, header=False, index=False, sep="|")
    
    # Verificación de Integridad del Sistema de Archivos
    if os.path.exists(target_path):
        size = os.path.getsize(target_path)
        print(f"✅ Éxito: Archivo escrito ({size} bytes).")
    else:
        raise Exception("Error crítico: El archivo no fue creado por el SO.")

# =================================================================
# ORQUESTACIÓN (CONTROL DE FLUJO)
# =================================================================

def run_full_pipeline():
    try:
        start_time = datetime.now()
        
        # Ejecución secuencial
        data_raw = extract(INPUT_FILE)
        data_clean = transform(data_raw)
        load(data_clean, OUTPUT_FILE)
        
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"🚀 Pipeline finalizado en {duration.total_seconds():.2f} segundos.")
        
    except Exception as error:
        print(f"🛑 [CRITICAL ERROR] Fallo en el pipeline: {error}")

if __name__ == "__main__":
    run_full_pipeline()
