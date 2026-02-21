# =================================================================
# EMPAQUETADO AUTOMÁTICO (AUTOLOGGING) CON MLFLOW Y SKLEARN
# =================================================================

# 1. Importamos el "Sabor" (Flavor) específico de scikit-learn dentro de MLflow.
# Los Flavors permiten estandarizar los modelos para su posterior despliegue.
import mlflow.sklearn

# 2. Establecemos el experimento como "Sklearn Model".
# Esto organiza nuestras ejecuciones dentro de un contenedor específico en el servidor de seguimiento.
mlflow.set_experiment("Sklearn Model")

# 3. Activamos el registro automático (autolog) para el sabor de scikit-learn.
# Esta función registrará automáticamente métricas (como R2), parámetros (como n_jobs) 
# y el objeto del modelo al llamar al método .fit().
mlflow.sklearn.autolog()

# Definición y entrenamiento del modelo (MLflow capturará todo aquí automáticamente)
lr = LinearRegression()
lr.fit(X_train, y_train)

# Obtener una predicción de los datos de prueba
print(lr.predict(X_test.iloc[[5]]))

# Autodocumentación:
# Gracias a mlflow.sklearn.autolog(), no necesitamos llamar a mlflow.start_run() 
# ni a los métodos log_* manualmente; el "Flavor" se encarga de la instrumentación.
