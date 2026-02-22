import pandas as pd
import sqlalchemy
import numpy as np

# =================================================================
# MÓDULO DE TRANSFORMACIÓN PROFESIONAL
# Propósito: Limpieza de datos, normalización de tipos y 
#            optimización de memoria para sistemas de producción.
# =================================================================

def extract_from_source(file_path):
    """Fase de Extracción: Carga de datos crudos."""
    print(f"📦 Extrayendo datos desde: {file_path}")
    if file_path.endswith('.parquet'):
        return pd.read_parquet(file_path, engine="fastparquet")
    return pd.read_csv(file_path)

def transform_data(df):
    """
    Fase de Transformación: El 'cerebro' del pipeline.
    Aquí aplicamos lógica de negocio y optimización de recursos.
    """
    print("🛠️ Iniciando proceso de transformación...")
    
    # 1. CONVERSIÓN DE TIPOS (Data Casting)
    # Por qué: Reducir memoria y habilitar operaciones temporales.
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%y %H:%M")
    
    # 2. FILTRADO DE FILAS (Data Cleaning)
    # Por qué: Eliminar ruido y registros que no cumplen la lógica de negocio.
    # Filtramos pedidos con cantidad > 1 y precio < 10 dólares.
    clean_df = df.loc[(df["Quantity Ordered"] > 1) & (df["Price Each"] < 10), :].copy()
    
    # 3. CÁLCULO DE MÉTRICAS (Feature Engineering)
    # Por qué: Generar valor añadido directamente en el pipeline.
    # Calculamos el total de la venta: Total = Cantidad * Precio
    clean_df["Total Sales"] = clean_df["Quantity Ordered"] * clean_df["Price Each"]
    
    # 4. PROYECCIÓN DE COLUMNAS (Dimensionality Reduction)
    # Por qué: Solo cargamos al destino lo que el analista realmente usará.
    final_columns = [
        "Order Date", 
        "Quantity Ordered", 
        "Price Each", 
        "Total Sales", 
        "Purchase Address"
    ]
    return clean_df.loc[:, final_columns]

def load_to_destination(df, target_file):
    """Fase de Carga: Persistencia de los datos procesados."""
    print(f"💾 Cargando datos transformados en: {target_file}")
    df.to_csv(target_file, index=False)
    print("✅ Proceso completado exitosamente.")

# =================================================================
# EJECUCIÓN DEL PIPELINE
# =================================================================

if __name__ == "__main__":
    # 1. Extraer
    raw_data = extract_from_source("sales_data.csv")
    
    # 2. Transformar
    transformed_data = transform_data(raw_data)
    
    # 3. Cargar
    load_to_destination(transformed_data, "cleaned_sales_report.csv")
    
    # Sanity Check para el Administrador
    print("\n--- RESUMEN DE TRANSFORMACIÓN ---")
    print(transformed_data.info()) # Muestra tipos de datos y uso de memoria
    print(transformed_data.head())
