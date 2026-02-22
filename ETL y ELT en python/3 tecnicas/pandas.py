import pandas as pd
import numpy as np

# 0. FUNCIÓN PERSONALIZADA (Lógica avanzada)
def find_street_name(address):
    """Extrae el nombre de la calle eliminando el número inicial."""
    if pd.isna(address):
        return "Unknown"
    # Dividimos por espacios y quitamos el primer elemento (el número)
    parts = address.split(' ')
    return ' '.join(parts[1:]) if len(parts) > 1 else address

# 1. PREPARACIÓN DE DATOS CRUDOS (Con ruidos y nulos)
data = {
    "street_address": ["111 Columbia Street", "350 Grand Street", "350 Grand Street", "120 Broadway", None],
    "city": ["Manhattan", "Manhattan", "Brooklyn", "Brooklyn", "Manhattan"],
    "math_score": [657.0, 395.0, np.nan, 418.0, 500.0],
    "reading_score": [601.0, np.nan, 428.0, 411.0, 520.0],
    "writing_score": [601.0, 387.0, 415.0, np.nan, 490.0]
}
raw_testing_scores = pd.DataFrame(data)

# =================================================================
# PIPELINE DE TRANSFORMACIÓN
# =================================================================

def transform_pipeline(df):
    # --- PASO A: Rellenar valores faltantes (Imputación por Media) ---
    # Calculamos la media de cada columna numérica para sanar el dataset
    df.fillna(
        value={
            "math_score": df["math_score"].mean(),
            "reading_score": df["reading_score"].mean(),
            "writing_score": df["writing_score"].mean()
        }, inplace=True
    )
    
    # --- PASO B: Transformación Avanzada (Apply) ---
    # Generamos una nueva característica (Feature Engineering)
    df["street_name"] = df.apply(
        lambda row: find_street_name(row["street_address"]),
        axis=1
    )
    
    # --- PASO C: Selección y Agrupamiento (Modeling) ---
    # Nos quedamos solo con lo necesario para el reporte por ciudad
    relevant_cols = ["city", "math_score", "reading_score", "writing_score"]
    grouped_report = df.loc[:, relevant_cols].groupby(by=["city"]).mean()
    
    return df, grouped_report

# =================================================================
# EJECUCIÓN Y RESULTADOS
# =================================================================

# Procesamos los datos
cleaned_data, city_report = transform_pipeline(raw_testing_scores)

print("🚀 DATOS LIMPIOS Y TRANSFORMADOS (Vista previa):")
print(cleaned_data[["street_name", "city", "math_score"]].head())

print("\n📊 REPORTE DE RENDIMIENTO POR CIUDAD (Agrupado):")
print(city_report)
