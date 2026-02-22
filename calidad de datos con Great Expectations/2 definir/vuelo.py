import pandas as pd
import great_expectations as gx
import logging

# Configuración de logs para trazabilidad (Estilo DevOps)
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_unified_gx_pipeline():
    # 1. PREPARACIÓN: Datos y Contexto
    # ---------------------------------------------------------
    context = gx.get_context()
    
    # Datos de simulación: Generación de Energía Renovable
    raw_data = {
        "timestamp": ["2026-02-21 12:00", "2026-02-21 13:00"],
        "energy_kwh": [450.5, 480.2],
        "temperature": [25.4, 26.1],
        "status": ["active", "active"]
    }
    df = pd.DataFrame(raw_data)

    # 2. CONEXIÓN: Data Source y Batch Definition
    # ---------------------------------------------------------
    # Definimos la infraestructura de datos
    ds = context.data_sources.add_pandas(name="energy_source")
    asset = ds.add_dataframe_asset(name="renewable_asset")
    batch_def = asset.add_batch_definition_whole_dataframe(name="full_batch_def")

    # 3. CREACIÓN DE EXPECTATIONS (Individuales)
    # ---------------------------------------------------------
    # Regla 1: Conteo exacto de columnas
    exp_col_count = gx.expectations.ExpectTableColumnCountToEqual(value=4)
    
    # Regla 2: Existencia de una columna crítica
    exp_col_name = gx.expectations.ExpectColumnToExist(column="temperature")
    
    # Regla 3: Rango de columnas (Flexibilidad de esquema)
    exp_col_range = gx.expectations.ExpectTableColumnCountToBeBetween(min_value=3, max_value=6)

    # 4. AGRUPACIÓN: Expectation Suite
    # ---------------------------------------------------------
    suite_name = "energy_quality_suite"
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))
    
    # Añadimos nuestras "leyes" al "libro"
    suite.add_expectation(exp_col_count)
    suite.add_expectation(exp_col_name)
    suite.add_expectation(exp_col_range)
    
    logging.info(f"✅ Suite '{suite_name}' creada con {len(suite.expectations)} reglas.")

    # 5. EJECUCIÓN MÉTODO A: Batch Validation (Modo Exploratorio/Dev)
    # ---------------------------------------------------------
    logging.info("\n--- Ejecutando Método A: Batch Validation ---")
    batch = batch_def.get_batch(batch_parameters={"dataframe": df})
    
    # Validamos la suite completa directamente sobre el batch
    results_a = batch.validate(expect=suite)
    print(f"Resultado Global: {'PASS' if results_a.success else 'FAIL'}")
    print(f"Estadísticas: {results_a.statistics}")

    # 6. EJECUCIÓN MÉTODO B: Validation Definition (Modo Producción/DevOps)
    # ---------------------------------------------------------
    logging.info("\n--- Ejecutando Método B: Validation Definition ---")
    
    val_def = gx.ValidationDefinition(
        data=batch_def,
        suite=suite,
        name="production_validation_contract"
    )
    
    # Ejecución formal usando la definición (persistible y automatizable)
    results_b = val_def.run(batch_parameters={"dataframe": df})
    
    # Inspección de un resultado específico (observed value)
    # Buscamos el resultado de la expectativa de conteo de columnas
    col_count_res = results_b.get_expectation_validation_result(
        expectation_type="expect_table_column_count_to_equal"
    )
    
    print(f"Estado Final: {'EXITOSO' if results_b.success else 'FALLIDO'}")
    print(f"Columnas detectadas: {col_count_res.result['observed_value']}")

    return results_b

# Ejecutar el proceso
if __name__ == "__main__":
    final_report = run_unified_gx_pipeline()
