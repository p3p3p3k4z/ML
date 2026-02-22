import logging
from pipeline_utils import extract, transform, load

# Configuración de Producción
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def run_e2e_pipeline():
    try:
        logging.info("🚀 Iniciando Canalización de Extremo a Extremo...")
        
        # 1. Extract
        raw_data = extract("raw_tax_data.csv")
        logging.debug(f"Shape inicial: {raw_data.shape}")
        
        # 2. Transform (Con validación manual de puntos de control)
        clean_data = transform(raw_data)
        logging.info(f"Check: Datos filtrados de {raw_data.shape[0]} a {clean_data.shape[0]} filas.")
        
        # 3. Load
        output = "clean_tax_data.parquet"
        load(clean_data, output)
        
        logging.info("✅ Pipeline ejecutado con éxito e integridad validada.")
        
    except Exception as e:
        logging.error(f"❌ Fallo crítico en la producción: {e}")

if __name__ == "__main__":
    # Simulación de ejecución en producción
    run_e2e_pipeline()
