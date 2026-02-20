Si la imputación era "llenar los huecos", el **escalado** es "nivelar el campo de juego". Como futuro ingeniero, sabes que no puedes comparar la temperatura de un servidor en grados Celsius con el tráfico de red en Gigabytes sin una métrica común. En Machine Learning, si tus características tienen rangos disparatados, el modelo se volverá "miope" y solo le prestará atención a los números más grandes.

---

## Centrado y Escalado de Datos (Feature Scaling)

### 1. ¿Por qué escalar los datos?

Muchos algoritmos de Machine Learning (especialmente **KNN, SVM y Regresión Lineal**) utilizan medidas de **distancia** para aprender.

- Si una característica como `duration_ms` varía de 0 a 1,000,000 y otra como `speechiness` varía de 0 a 1, el algoritmo asumirá que la duración es un millón de veces más importante solo porque sus números son mayores.
    

**Objetivo:** Transformar todas las características para que tengan una escala similar, permitiendo que el modelo aprenda de la importancia real de cada variable y no de su magnitud nominal.

---

### 2. Métodos Comunes de Escalado

#### A. Estandarización (Standardization)

Transforma los datos para que tengan una **media de 0** y una **varianza de 1**. Es el método más común y se calcula como:

$$z = \frac{x - \mu}{\sigma}$$

Donde $x$ es el valor original, $\mu$ la media y $\sigma$ la desviación estándar.

#### B. Normalización (Min-Max Scaling)

Escala los datos a un rango fijo, generalmente entre **0 y 1**.

$$x_{scaled} = \frac{x - x_{min}}{x_{max} - x_{min}}$$

---

### 3. Implementación en Scikit-learn

El flujo de trabajo profesional siempre incluye el escalado **después** del `train_test_split` para evitar que la información del conjunto de prueba (como su media) se filtre en el entrenamiento.


```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 1. División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Instanciar y ajustar el escalador
scaler = StandardScaler()

# 3. Fit_transform en entrenamiento, pero SOLO transform en prueba
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

---

### 4. Escalado y Optimización en Canalizaciones (Pipelines)

El verdadero poder surge al combinar el escalado con `GridSearchCV` dentro de un `Pipeline`. Esto permite optimizar el modelo mientras nos aseguramos de que cada pliegue de la validación cruzada se escale correctamente.

#### Código: Pipeline con Tuning de Hiperparámetros

```python
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

# 1. Definir los pasos (Escalado + Modelo)
steps = [("scaler", StandardScaler()),
         ("knn", KNeighborsClassifier())]
pipeline = Pipeline(steps)

# 2. Definir la rejilla de parámetros
# NOTA: Usamos 'nombre_paso__nombre_parametro' (doble guion bajo)
parameters = {"knn__n_neighbors": np.arange(1, 20)}

# 3. Instanciar GridSearchCV con el Pipeline
cv = GridSearchCV(pipeline, param_grid=parameters)

# 4. Ajustar y evaluar
cv.fit(X_train, y_train)
y_pred = cv.predict(X_test)

print("Mejores parámetros: {}".format(cv.best_params_))
print("Mejor puntuación (Accuracy): {}".format(cv.best_score_))
```

---

### Notas de Ingeniería (Enfoque DevOps)

- **Impacto Real:** En el ejemplo del curso, el uso de datos sin escalar en KNN daba una precisión de **0.53**, mientras que el simple hecho de añadir un `StandardScaler` la subió a **0.81**. ¡Una mejora del 50% sin cambiar de algoritmo!
    
- **Consistencia:** En un entorno de producción, el objeto `scaler` que "aprendió" la media y desviación del entrenamiento debe ser el mismo que transforme los datos en tiempo real. Si escalas cada nueva solicitud de usuario de forma aislada, el modelo recibirá basura.
    
- **Robustez:** La estandarización es generalmente preferible si tus datos tienen valores atípicos (_outliers_), ya que no los comprime en un rango min-max pequeño, manteniendo mejor la distribución original.
    