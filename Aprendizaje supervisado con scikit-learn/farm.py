import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

# 1. Cargar el conjunto de datos
crops = pd.read_csv("soil_measures.csv")

# 2. Análisis rápido de integridad (Recomendado en ingeniería de datos)
# Verificamos si hay valores nulos
print(crops.isna().sum())

# 3. Preparación de los datos
# Definimos X (características) e y (objetivo)
X = crops.drop("crop", axis=1)
y = crops["crop"]

# Dividimos en entrenamiento y prueba (80/20)
# Usamos random_state=42 para reproducibilidad, vital en MLOps
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Evaluación de características individuales
# Creamos un diccionario para almacenar el rendimiento de cada sensor
feature_performance = {}

# Iteramos sobre cada columna de características
for feature in ["N", "P", "K", "ph"]:
    # Instanciamos el modelo de Regresión Logística
    # multi_class="multinomial" es necesario para clasificar múltiples tipos de cultivos
    # max_iter=2000 asegura que el algoritmo converja con una sola variable
    log_reg = LogisticRegression(max_iter=2000, multi_class="multinomial")
    
    # Entrenamos el modelo usando SOLO la característica actual
    # Usamos [[feature]] para pasar un DataFrame de una sola columna
    log_reg.fit(X_train[[feature]], y_train)
    
    # Realizamos predicciones sobre el conjunto de prueba
    y_pred = log_reg.predict(X_test[[feature]])
    
    # Calculamos el F1-score ponderado
    # Esta métrica es preferible a la Accuracy cuando hay clases desequilibradas
    f1 = metrics.f1_score(y_test, y_pred, average="weighted")
    
    # Guardamos el resultado
    feature_performance[feature] = f1
    print(f"Rendimiento de {feature} (F1-score): {f1:.4f}")

# 5. Identificar la mejor característica predictiva
# Buscamos la clave con el valor máximo en nuestro diccionario
best_feature = max(feature_performance, key=feature_performance.get)
best_score = feature_performance[best_feature]

# Creamos la variable final solicitada por el proyecto
best_predictive_feature = {best_feature: best_score}

print("-" * 30)
print(f"Resultado final: {best_predictive_feature}")
