# =================================================================
# CARGA DE MODELOS POR ETAPA DESDE EL MODEL REGISTRY
# =================================================================

# 1. Cargamos el modelo "Insurance" en su etapa de producción.
# Usamos el sabor 'sklearn' y el URI con el formato "models:/nombre/etapa".
# Esta es la forma más limpia de conectar una aplicación con el mejor modelo disponible.
model = mlflow.sklearn.load_model("models:/Insurance/Production")

# 2. Ejecutamos la predicción sobre los datos de prueba X_test.
# El modelo cargado se comporta como un objeto nativo de scikit-learn,
# permitiendo realizar inferencias de forma inmediata.
model.predict(X_test)

# Autodocumentación:
# Al utilizar el URI "models:/Insurance/Production", el sistema siempre 
# descargará la versión que el administrador del registro haya marcado 
# como estable, sin necesidad de cambiar el código de la aplicación cliente.
