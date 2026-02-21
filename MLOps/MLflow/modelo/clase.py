# =================================================================
# CREACIÓN DE MODELOS PERSONALIZADOS (CUSTOM PYTHON CLASS)
# =================================================================

# Definimos una clase personalizada que hereda de mlflow.pyfunc.PythonModel
# Esta clase permite estandarizar modelos con lógica personalizada.
class CustomPredict(mlflow.pyfunc.PythonModel):
    
    # El método load_context() se ejecuta automáticamente cuando el modelo se carga.
    # Se utiliza para cargar artefactos (como el binario del modelo) desde una ruta específica.
    def load_context(self, context):
        # Cargamos un modelo de scikit-learn previamente guardado en el directorio local.
        self.model = mlflow.sklearn.load_model("./lr_model/")
        
    # El método predict() define la lógica de inferencia personalizada.
    # Recibe el contexto y los datos de entrada (model_input) para generar la salida.
    def predict(self, context, model_input):
        # 1. Obtenemos las predicciones numéricas crudas del modelo cargado.
        predictions = self.model.predict(model_input)
        
        # 2. Lógica de decodificación: convertimos valores numéricos en etiquetas legibles.
        # Esto es parte de la personalización del modelo para facilitar su uso final.
        decoded_predictions = []  
        for prediction in predictions:
            if prediction == 0:
                decoded_predictions.append("female")
            else:
                decoded_predictions.append("male")
                
        # Retornamos las etiquetas ya decodificadas.
        return decoded_predictions

# Autodocumentación:
# Al heredar de PythonModel, esta clase puede ser empaquetada y desplegada 
# utilizando el "sabor" (flavor) pyfunc de MLflow, garantizando que la 
# lógica de decodificación acompañe siempre al modelo en producción.
