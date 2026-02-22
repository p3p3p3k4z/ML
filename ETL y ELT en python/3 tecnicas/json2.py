import pandas as pd
import json

# =================================================================
# 1. FUENTE DE DATOS (Simulación de JSON anidado)
# =================================================================
raw_testing_scores = {
    "01M539": {
        "street_address": "111 Columbia Street",
        "city": "Manhattan",
        "scores": {"math": 657, "reading": 601} # Falta 'writing' intencionalmente
    },
    "02M400": {
        "street_address": "200 Second Ave",
        "city": "Manhattan",
        "scores": {"math": 540, "reading": 520, "writing": 510}
    }
}

# =================================================================
# 2. TRANSFORMACIÓN Y ANÁLISIS (Data Flattening)
# =================================================================
def normalize_school_data(nested_dict):
    normalized_list = []
    
    print("🔍 Iniciando iteración de diccionarios...")
    
    # Usamos .items() para obtener la LLAVE (ID) y el VALOR (Info) simultáneamente
    for school_id, school_info in nested_dict.items():
        
        # Extracción segura con .get() para evitar KeyErrors
        address = school_info.get("street_address", "N/A")
        city = school_info.get("city", "Unknown")
        
        # Acceso a diccionario anidado 'scores'
        # Usamos un paracaídas: si 'scores' no existe, devolvemos un dict vacío {}
        scores = school_info.get("scores", {})
        
        # Extraemos materias con valor por defecto 0 si no existen
        m_score = scores.get("math", 0)
        r_score = scores.get("reading", 0)
        w_score = scores.get("writing", 0)
        
        # Construimos la fila (lista) para nuestra futura tabla
        normalized_list.append([school_id, address, city, m_score, r_score, w_score])
        
    return normalized_list

# Ejecutamos la normalización
flat_data = normalize_school_data(raw_testing_scores)

# =================================================================
# 3. CARGA Y LIMPIEZA FINAL (Pandas)
# =================================================================

# Convertimos la lista de listas en un DataFrame
df = pd.DataFrame(flat_data)

# Asignamos nombres de columnas profesionales (Snake Case)
df.columns = [
    "school_id", "street_address", "city", 
    "avg_math", "avg_reading", "avg_writing"
]

# Establecemos el school_id como índice para búsquedas rápidas (O(1))
df.set_index("school_id", inplace=True)

# Cálculo de valor agregado: Puntaje Total
# Usamos LaTeX para representar la lógica: $Total = Math + Reading + Writing$
df["total_score"] = df["avg_math"] + df["avg_reading"] + df["avg_writing"]

print("\n✅ DataFrame Finalizado y Limpio:")
print(df.head())
