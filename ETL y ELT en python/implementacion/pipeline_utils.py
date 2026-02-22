import pandas as pd
import sqlalchemy
import logging

def extract(file_path):
    """Extrae datos (Simulado para el ejercicio)."""
    # En producción esto leería de un CSV o JSON
    data = {
        "industry_name": ["Tech", "Agro", "Retail", "Tech", "Agro"],
        "total_taxable_income": [100000, 50000, 120000, 80000, 40000],
        "number_of_firms": [10, 5, 12, 8, 4],
        "total_taxes_paid": [20000, 5000, 24000, 15000, 4000]
    }
    return pd.DataFrame(data)

def transform(raw_data):
    """Transformación con Puntos de Control y Feature Engineering."""
    # Checkpoint 1: Validar que la entrada sea un DataFrame
    assert isinstance(raw_data, pd.DataFrame), "La entrada no es un DataFrame"
    
    # Feature Engineering: Crear nueva columna
    raw_data["average_taxable_income"] = raw_data["total_taxable_income"] / raw_data["number_of_firms"]
    
    # Checkpoint 2: Validación lógica (Assert)
    # Filtramos industrias con ingreso promedio > 100
    clean_data = raw_data.loc[raw_data["average_taxable_income"] > 100, :].copy()
    
    # Calculamos tax_rate
    clean_data["tax_rate"] = clean_data["total_taxes_paid"] / clean_data["total_taxable_income"]
    
    clean_data.set_index("industry_name", inplace=True)
    return clean_data

def load(clean_data, output_path):
    """Carga Idempotente en Parquet."""
    # El modo de escritura en Parquet por defecto sobrescribe (Idempotencia)
    clean_data.to_parquet(output_path)
