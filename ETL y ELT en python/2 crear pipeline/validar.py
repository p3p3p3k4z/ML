import pandas as pd

# =================================================================
# PIPELINE ETL CON VALIDACIÓN DE CALIDAD (DATA OBSERVABILITY)
# Propósito: Extraer datos Parquet, filtrar pedidos unitarios 
#            y validar que el resultado cumpla los estándares.
# =================================================================

def extract(file_path):
    """
    Fase de Extracción: Lectura de formato columnar.
    POR QUÉ: Parquet es más eficiente que CSV para grandes volúmenes.
    """
    print(f"📦 [EXTRACT] Leyendo archivo: {file_path}")
    try:
        # Usamos read_parquet para mantener los tipos de datos nativos
        return pd.read_parquet(file_path)
    except Exception as e:
        print(f"❌ Error en extracción: {e}")
        return None

def transform(raw_data):
    """
    Fase de Transformación: Poda de datos.
    POR QUÉ: Reducir la dimensionalidad mejora el rendimiento del sistema.
    """
    print("🛠️ [TRANSFORM] Filtrando pedidos unitarios y seleccionando columnas...")
    
    # Filtramos filas: Solo Quantity Ordered == 1
    # Seleccionamos columnas: Order ID, Price Each, Quantity Ordered
    clean_data = raw_data.loc[
        raw_data["Quantity Ordered"] == 1, 
        ["Order ID", "Price Each", "Quantity Ordered"]
    ]
    return clean_data

def validate(df):
    """
    Fase de Validación (Sanity Check):
    POR QUÉ: En DevOps, 'fallar rápido' es mejor que cargar datos erróneos.
    """
    print("⚖️ [VALIDATE] Iniciando pruebas de calidad de datos...")
    
    # 1. Validación de Integridad: ¿El DataFrame está vacío?
    if df.empty:
        print("⚠️ Advertencia: El DataFrame resultante no tiene registros.")
        return False
    
    # 2. Validación de Filtro: ¿Realmente solo hay pedidos de cantidad 1?
    # Usamos .unique() para verificar los valores distintos en la columna
    unique_quantities = df["Quantity Ordered"].unique()
    if len(unique_quantities) == 1 and unique_quantities[0] == 1:
        print("✅ Prueba de Filtro: PASADA (Solo valores de 1 encontrados).")
    else:
        print(f"❌ Prueba de Filtro: FALLIDA. Valores encontrados: {unique_quantities}")
        return False

    # 3. Validación de Nulos: ¿Hay datos faltantes en columnas críticas?
    null_counts = df.isnull().sum().sum()
    if null_counts == 0:
        print("✅ Prueba de Nulos: PASADA (0 valores nulos).")
    else:
        print(f"❌ Prueba de Nulos: FALLIDA. Se encontraron {null_counts} nulos.")
        return False

    print("🚀 Validación completa: Datos listos para la carga.")
    return True

# =================================================================
# ORQUESTACIÓN PRINCIPAL
# =================================================================

# 1. Extraer
raw_sales_data = extract("sales_data.parquet")

if raw_sales_data is not None:
    # 2. Transformar
    clean_sales_data = transform(raw_sales_data)
    
    # 3. Validar
    # Solo si la validación es exitosa, procederíamos al siguiente paso (Load)
    if validate(clean_sales_data):
        print("\n--- RESUMEN FINAL ---")
        print(clean_sales_data.head())
        print(f"Total de registros validados: {len(clean_sales_data)}")
    else:
        print("🛑 Proceso detenido: Los datos transformados no pasaron las pruebas.")
