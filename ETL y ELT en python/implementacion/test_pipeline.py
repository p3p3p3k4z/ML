import pytest
import pandas as pd
from pipeline_utils import extract, transform

# 1. FIXTURE: Prepara los datos para todas las pruebas
@pytest.fixture
def raw_tax_data():
    return extract("mock_path.csv")

# 2. PRUEBA UNITARIA: Validar la transformación
def test_transformed_data(raw_tax_data):
    clean_data = transform(raw_tax_data)
    
    # Validación de instancia
    assert isinstance(clean_data, pd.DataFrame)
    
    # Validación de lógica: El tax_rate debe estar entre 0 y 1
    # $0 \leq tax\_rate \leq 1$
    assert clean_data["tax_rate"].max() <= 1
    assert clean_data["tax_rate"].min() >= 0
    
    # Validación de estructura: Debe tener más columnas que el original 
    # (considerando que industry_name se fue al índice)
    assert "average_taxable_income" in clean_data.columns
