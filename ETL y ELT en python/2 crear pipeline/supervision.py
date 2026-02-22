import pandas as pd
import logging
import os

# =================================================================
# CONFIGURACIÓN DE SUPERVISIÓN (LOGGING)
# POR QUÉ: Establecemos DEBUG para capturar cada detalle en desarrollo.
# En producción, podrías cambiarlo a INFO o WARNING.
# =================================================================
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract(file_path):
    """
    EXTRACCIÓN: Carga segura de archivos.
    """
    try:
        logging.debug(f"Intentando leer: {file_path}")
        return pd.read_parquet(file_path)
    except FileNotFoundError as e:
        logging.error(f"Error Crítico: El archivo no existe en la ruta {file_path}. Detalle: {e}")
        return None

def transform(raw_data):
    """
    TRANSFORMACIÓN: Lógica de negocio con autorreparación (Self-Healing).
    """
    logging.debug(f"Forma del DataFrame antes de filtrar: {raw_data.shape}")
    
    # 1. Transformación de tipos
    raw_data["Order Date"] = pd.to_datetime(raw_data["Order Date"], format="%m/%d/%y %H:%M")
    logging.info("Columna 'Order Date' convertida exitosamente a datetime.")

    # 2. Supervisión de Columnas y Filtrado
    try:
        # Intentamos filtrar por 'Total Price'
        clean_data = raw_data.loc[raw_data["Total Price"] > 1000, :]
        logging.info("Filtrado exitoso por 'Total Price' > 1000.")
        
    except KeyError as ke:
        # ESTRATEGIA DE REPARACIÓN: Si la columna no existe, la creamos
        logging.warning(f"Excepción capturada: {ke}. La columna 'Total Price' no existe. Iniciando autorreparación...")
        
        # Calculamos el Precio Total: Cantidad * Precio Unitario
        raw_data["Total Price"] = raw_data["Price Each"] * raw_data["Quantity Ordered"]
        
        # Reintentamos la transformación después de la reparación
        clean_data = raw_data.loc[raw_data["Total Price"] > 1000, :]
        logging.info("DataFrame reparado y filtrado correctamente tras KeyError.")

    logging.debug(f"Forma del DataFrame después de filtrar: {clean_data.shape}")
    return clean_data

# =================================================================
# ORQUESTACIÓN Y ALERTAS
# =================================================================

def run_pipeline():
    # 1. Ejecutar Extracción
    raw_sales_data = extract("sales_data.parquet")
    
    if raw_sales_data is not None:
        try:
            # 2. Ejecutar Transformación
            clean_sales_data = transform(raw_sales_data)
            
            # 3. Alerta de éxito final
            print("🚀 Pipeline ejecutado: Datos listos para el análisis.")
            logging.info(f"Proceso finalizado. Registros procesados: {len(clean_sales_data)}")
            
        except Exception as general_error:
            # Captura de errores no previstos (Panic log)
            logging.critical(f"Fallo inesperado en el pipeline: {general_error}")
    else:
        logging.warning("El pipeline se detuvo en la fase de extracción: Fuente no encontrada.")

if __name__ == "__main__":
    run_pipeline()
