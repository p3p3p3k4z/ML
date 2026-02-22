import pandas as pd
import great_expectations as gx
import logging

# Configuración de logging para monitoreo tipo DevOps
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def setup_gx_environment():
    """
    Bloque 1: Inicialización del Data Context (El Cerebro)
    Temas: Crea tu Data Context, Vista previa de GX.
    """
    logging.info("⚙️ Inicializando el Data Context...")
    # El Contexto gestiona configuraciones, metadatos y almacenamiento de resultados
    context = gx.get_context()
    return context

def connect_to_data(context, dataframe):
    """
    Bloque 2: Conexión con los Datos (La Tubería)
    Temas: Conectar con los datos, Crea una Data Source y un Data Asset.
    """
    logging.info("🔗 Configurando Data Source y Data Asset...")
    
    # 1. Data Source: Define el motor de ejecución (Pandas)
    data_source = context.data_sources.add_pandas(name="weather_datasource")
    
    # 2. Data Asset: Define el recurso lógico (El 'Tanque' de datos)
    data_asset = data_source.add_dataframe_asset(name="daily_weather_asset")
    
    return data_asset

def create_and_inspect_batch(data_asset, df_puro):
    """
    Bloque 3: Batch Definition e Inspección (La Muestra)
    Temas: Crea una Batch Definition y un Batch, Inspecciona tu Batch.
    """
    logging.info("📦 Generando Batch para validación...")
    
    # 1. Batch Definition: La 'receta' para seleccionar datos
    # Usamos 'whole_dataframe' para tomar todo el conjunto actual
    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        name="full_dataset_batch_def"
    )
    
    # 2. El Batch: Los datos 'vivos' con metadatos de GX
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df_puro})
    
    # --- INSPECCIÓN TÉCNICA (Sanity Checks) ---
    logging.info("🔍 Inspeccionando el Batch...")
    
    cols = batch.columns()
    print(f"✅ Columnas detectadas: {cols}")
    
    # Verificamos las primeras 5 filas para validación visual
    preview = batch.head(n_rows=5)
    print("\n--- VISTA PREVIA DEL BATCH ---")
    print(preview)
    
    return batch

# ==========================================
# EJECUCIÓN DEL FLUJO UNIFICADO
# ==========================================
if __name__ == "__main__":
    # Simulación: Datos meteorológicos de la Mixteca
    weather_data = {
        "fecha": ["2026-02-21", "2026-02-22", "2026-02-23"],
        "temp_max": [28.5, 30.2, 27.8],
        "humedad": [45, 40, 50]
    }
    df = pd.DataFrame(weather_data)

    # 1. Iniciar sesión (Data Context)
    my_context = setup_gx_environment()

    # 2. Conectar tuberías (Source & Asset)
    my_asset = connect_to_data(my_context, df)

    # 3. Obtener e inspeccionar el lote (Batch)
    my_batch = create_and_inspect_batch(my_asset, df)
    
    logging.info("🚀 ¡Entorno GX listo para aplicar Expectations!")
