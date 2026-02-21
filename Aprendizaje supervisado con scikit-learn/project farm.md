Este es un excelente proyecto de **Selección de Características (Feature Selection)**. Como experto en Machine Learning, tu objetivo es determinar cuál de los parámetros del suelo (Nitrógeno, Fósforo, Potasio o pH) es el "ganador" en términos de poder predictivo individual.

Este problema es muy común en **ingeniería de datos y despliegue (DevOps)**: a veces, por presupuesto o latencia, no podemos recolectar todos los datos y debemos elegir el sensor más eficiente.


---

## 🌾 Proyecto: Identificación de la Mejor Característica Predictiva

### 1. Diagnóstico y Preparación

Primero, cargamos los datos y realizamos una revisión rápida. Siguiendo tus apuntes previos, lo primero es verificar si existen valores nulos que requieran un `SimpleImputer`.

```python
# 1. Carga de datos y revisión rápida
crops = pd.read_csv("soil_measures.csv")

# Verificar nulos (Basado en tu apunte de preprocesamiento)
print(crops.isna().sum())

# Verificar tipos de cultivos (Target)
print(crops["crop"].unique())
```

### 2. División de Datos (Train/Test Split)

Separamos el conjunto de datos para asegurar que nuestra evaluación sea honesta y evitar el **Data Leakage**.

```python
# 2. Definir X e y
X = crops.drop("crop", axis=1)
y = crops["crop"]

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### 3. Evaluación de Características Individuales

Aquí aplicamos un bucle para entrenar un modelo de **Regresión Logística** utilizando **solo una característica a la vez**. Calcularemos el **F1-score**, que es ideal para clasificación multiclase ya que equilibra la precisión y la sensibilidad (Recall).

```python
# 3. Evaluar cada característica por separado
feature_performance = {}

for feature in ["N", "P", "K", "ph"]:
    # Instanciar el modelo (Usando multinomial para multiclase)
    log_reg = LogisticRegression(max_iter=2000, multi_class="multinomial")
    
    # Entrenar usando solo una columna de X_train
    log_reg.fit(X_train[[feature]], y_train)
    
    # Predecir y evaluar
    y_pred = log_reg.predict(X_test[[feature]])
    
    # Usamos el F1-score ponderado (weighted) como métrica de éxito
    score = metrics.f1_score(y_test, y_pred, average="weighted")
    
    feature_performance[feature] = score
    print(f"F1-score para {feature}: {score:.4f}")
```

### 4. Selección del Ganador

Finalmente, identificamos cuál obtuvo el puntaje más alto y lo almacenamos en el formato de diccionario solicitado.

```python
# 4. Encontrar la mejor característica
best_feature = max(feature_performance, key=feature_performance.get)
best_score = feature_performance[best_feature]

# Crear la variable final
best_predictive_feature = {best_feature: best_score}

print(f"\n✅ La mejor característica es: {best_predictive_feature}")
```

---

## 🧠 Análisis Técnico para tu Carrera

Desde la perspectiva de **Ingeniería y MLOps**, este ejercicio nos enseña tres cosas fundamentales:

1. **Eficiencia de Costos:** Al identificar que (por ejemplo) el **Potasio (K)** o el **Nitrógeno (N)** tienen un 70% de precisión por sí solos, el granjero puede ahorrar el 75% de su presupuesto de sensores sacrificando solo un margen aceptable de error.
    
2. **Métrica $F1-Score$:** En problemas multiclase con cultivos, no usamos solo _Accuracy_. El F1-score es la media armónica entre precisión y recall, lo que nos asegura que el modelo es bueno identificando todos los tipos de cultivos, no solo el más frecuente.
    
    $$F1 = 2 \cdot \frac{\text{precisión} \cdot \text{recall}}{\text{precisión} + \text{recall}}$$
    
3. **Iteración de Modelos:** Este patrón de "probar y guardar en un diccionario" es el mismo que usamos en `GridSearchCV` para encontrar hiperparámetros. Estás automatizando la toma de decisiones.
    
