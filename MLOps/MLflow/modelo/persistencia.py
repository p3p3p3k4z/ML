# =================================================================
# PERSISTENCIA LOCAL DE MODELOS CON MLFLOW (SKLEARN FLAVOR)
# =================================================================

# 1. Cargamos el modelo existente desde el sistema de archivos local.
# Usamos el "sabor" sklearn y la función load_model indicando la ruta del directorio.
# Esto permite la reproducibilidad al recuperar versiones previas del modelo[cite: 5, 45].
model = mlflow.sklearn.load_model("lr_local_v1")

# --- Bloque de Entrenamiento (Contexto del Ejercicio) ---
# Datos de entrenamiento
X = df[["R&D Spend", "Administration", "Marketing Spend", "State"]]
y = df[["Profit"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=0)

# Entrenamos el modelo cargado con los nuevos datos (Retraining)
model.fit(X_train, y_train)
# -------------------------------------------------------

# 2. Guardamos el nuevo modelo entrenado localmente.
# Usamos save_model para empaquetar el objeto del modelo y sus dependencias en un nuevo directorio.
# Este paquete ahora está listo para ser compartido o desplegado[cite: 5, 42].
mlflow.sklearn.save_model(model, "lr_local_v2")

# Autodocumentación:
# Al usar mlflow.sklearn, el modelo se guarda con un formato estándar que incluye 
# los metadatos necesarios para que cualquier otro entorno compatible pueda cargarlo[cite: 5, 91].
