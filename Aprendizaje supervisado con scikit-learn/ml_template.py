import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib  # Para guardar el modelo (DevOps focus)
from sklearn.model_selection import train_test_split, KFold, GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    root_mean_squared_error, r2_score
)
# Modelos
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# ==========================================
# 1. CARGA Y PREPROCESAMIENTO INICIAL
# ==========================================
# Cargar datos
df = pd.read_csv("tu_dataset.csv")

# A. Manejo de Categorías (Variables Ficticias)
# Aplicamos la regla N-1 para evitar redundancia
df_processed = pd.get_dummies(df, drop_first=True)

# B. Definir X e y
# Cambia 'target_column' por el nombre de tu columna objetivo
X = df_processed.drop("target_column", axis=1).values
y = df_processed["target_column"].values

# C. División de datos (Split)
# Reservamos el test set para el final (Hold-out set)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y # stratify solo para clasificación
)

# ==========================================
# 2. CONSTRUCCIÓN DE LA CANALIZACIÓN (PIPELINE)
# ==========================================
# Definimos los pasos: Imputación -> Escalado -> Modelo
# Puedes cambiar el modelo según el problema (LogReg, KNN, Ridge, etc.)
steps = [
    ("imputer", SimpleImputer(strategy="median")), # Manejo de nulos
    ("scaler", StandardScaler()),                 # Centrado y escalado
    ("model", LogisticRegression())               # El estimador final
]

pipeline = Pipeline(steps)

# ==========================================
# 3. OPTIMIZACIÓN (HYPERPARAMETER TUNING)
# ==========================================
# Definimos el espacio de búsqueda
# NOTA: Usar nombre_del_paso__nombre_parametro
param_grid = {
    "model__C": np.linspace(0.001, 1.0, 10),
    "model__solver": ["lbfgs", "liblinear"],
    "imputer__strategy": ["mean", "median"] # ¡También podemos tunear el preprocesamiento!
}

# Validación Cruzada (K-Fold)
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Búsqueda en Cuadrícula (GridSearchCV)
# Cambia a RandomizedSearchCV si el espacio es muy grande
search = GridSearchCV(pipeline, param_grid=param_grid, cv=kf, scoring="accuracy")

# Entrenar todo el flujo
search.fit(X_train, y_train)

# ==========================================
# 4. EVALUACIÓN FINAL (MODELO GANADOR)
# ==========================================
print(f"Mejores parámetros: {search.best_params_}")
print(f"Mejor score de CV: {search.best_score_:.4f}")

# Predecir con el conjunto de prueba
y_pred = search.predict(X_test)
y_pred_probs = search.predict_proba(X_test)[:, 1] # Para ROC AUC

# Métricas de Clasificación
print("\n--- Matriz de Confusión ---")
print(confusion_matrix(y_test, y_pred))
print("\n--- Reporte de Clasificación ---")
print(classification_report(y_test, y_pred))
print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_probs):.4f}")

# ==========================================
# 5. PERSISTENCIA (GUARDAR PARA PRODUCCIÓN)
# ==========================================
# Esto guarda el Pipeline COMPLETO (Imputer + Scaler + Model)
joblib.dump(search.best_estimator_, "modelo_final.pkl")
print("\n✅ Modelo guardado exitosamente como 'modelo_final.pkl'")
