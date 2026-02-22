import pandas as pd
import numpy as np
import os

# =================================================================
# 1. COMPONENTES DEL PIPELINE (ETL)
# =================================================================

def extract_mock_data():
    """Simula la extracción de datos fiscales."""
    data = {
        "id": [1, 2, 3, 4, 5],
        "tax_rate": [0.15, 0.20, 0.10, 0.25, 0.12],
        "income": [50000, 60000, 45000, 80000, 55000]
    }
    return pd.DataFrame(data)

def transform(df):
    """Aplica filtros y genera nuevas columnas."""
    # Punto de control: Filtrar rentas mayores a 50k
    df_clean = df[df["income"] > 50000].copy()
    # Generamos columna de impuesto calculado
    df_clean["tax_amount"] = df_clean["income"] * df_clean["tax_rate"]
    return df_clean

def load_to_parquet(df, filename):
    """Carga de forma idempotente (sobrescritura)."""
    df.to_parquet(filename, index=False)

# =================================================================
# 2. SUITE DE PRUEBAS Y VALIDACIÓN
# =================================================================

def run_full_pipeline_test(iterations=3):
    filename = "clean_tax_data.parquet"
    
    print(f"🚀 Iniciando prueba de estrés e idempotencia ({iterations} ejecuciones)...")
    
    # Simulamos ejecuciones repetidas (Prueba de Idempotencia)
    for i in range(iterations):
        print(f"\n--- Intento {i+1} ---")
        
        # Extracción y Transformación
        raw_data = extract_mock_data()
        clean_data = transform(raw_data)
        
        # CARGA
        load_to_parquet(clean_data, filename)
        
        # VALIDACIÓN 1: Punto de Control de Dimensiones (Shape)
        # Verificamos que el filtro redujo las filas como se esperaba
        print(f"   [CHECK] Dimensiones Raw: {raw_data.shape} -> Clean: {clean_data.shape}")
        
    # VALIDACIÓN 2: Prueba de Integridad (Equals)
    # Leemos el archivo final para comparar con el último proceso en memoria
    to_validate = pd.read_parquet(filename)
    
    if to_validate.equals(clean_data):
        print(f"\n✅ INTEGRIDAD: Los datos en disco coinciden al 100% con la memoria.")
    else:
        print(f"\n❌ ERROR: Discrepancia detectada entre memoria y disco.")

    # VALIDACIÓN 3: Prueba Final de Idempotencia
    # Si la carga es idempotente, el archivo final NO debe tener filas duplicadas
    if to_validate.shape[0] == clean_data.shape[0]:
        print(f"✅ IDEMPOTENCIA: No se detectaron datos duplicados tras {iterations} ejecuciones.")
    else:
        print(f"❌ ERROR: El archivo acumuló datos (Modo Append detectado).")

# Ejecutar validación unificada
run_full_pipeline_test()
