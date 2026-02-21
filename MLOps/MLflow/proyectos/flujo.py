# =================================================================
# ORQUESTADOR MAESTRO: PIPELINE DE ML PARA EL PROYECTO "INSURANCE"
# =================================================================
import mlflow

def run_pipeline():
    print("🚀 Iniciando Pipeline de ML...")

    # --- PASO 1: INGENIERÍA DE MODELOS (ENTRENAMIENTO) ---
    print("\n[1/2] Ejecutando Ingeniería de Modelos...")
    
    # Lanzamos el entrenamiento y capturamos el objeto de ejecución
    model_eng_execution = mlflow.projects.run(
        uri='./',
        entry_point='model_engineering',
        experiment_name='Insurance',
        parameters={
            'n_jobs': 2, 
            'fit_intercept': False
        },
        env_manager='local',
        synchronous=True  # Esperamos a que termine para obtener el ID
    )
    
    # Extraemos el ID único de esta ejecución (el "token" de trazabilidad)
    model_eng_run_id = model_eng_execution.run_id
    print(f"✅ Entrenamiento completado. Run ID: {model_eng_run_id}")

    # --- PASO 2: EVALUACIÓN DEL MODELO ---
    print("\n[2/2] Ejecutando Evaluación del Modelo...")
    
    # Pasamos el ID del paso anterior como parámetro de entrada
    model_eval_execution = mlflow.projects.run(
        uri="./",
        entry_point="model_evaluation",
        parameters={
            "run_id": model_eng_run_id,
        },
        env_manager="local",
        synchronous=True
    )

    # --- FINALIZACIÓN Y REPORTE ---
    status = model_eval_execution.get_status()
    print(f"\n✨ Pipeline finalizado con estado: {status}")

if __name__ == "__main__":
    run_pipeline()
