En este ejercicio, aplicaremos una **Regresión Lasso** para predecir el volumen (_loudness_) de las canciones. Es importante recordar que Lasso aplica una penalización a los coeficientes del modelo; por lo tanto, si las características no están en la misma escala, el modelo podría penalizar injustamente a variables con rangos pequeños. El uso de `StandardScaler` dentro de un `Pipeline` garantiza que todas las variables contribuyan de manera equitativa antes de que Lasso realice la selección de características.

```python
# Importar StandardScaler desde sklearn.preprocessing
from sklearn.preprocessing import StandardScaler

# 1. Crear los pasos para el objeto canalización
# Incluimos el escalador y el modelo Lasso con alpha=0.5
steps = [("scaler", StandardScaler()),
         ("lasso", Lasso(alpha=0.5))]

# 2. Instanciar la canalización con los pasos definidos
pipeline = Pipeline(steps)

# 3. Ajustar la canalización a los datos de entrenamiento
pipeline.fit(X_train, y_train)

# 4. Calcular e imprimir el valor R-cuadrado en los datos de prueba
# El método .score() en regresión devuelve el coeficiente de determinación R^2
print(pipeline.score(X_test, y_test))
```

---

### Análisis del Ejercicio: Lasso y Escalado

Para tu formación técnica, este flujo de trabajo es el estándar de oro por varias razones:

#### 1. Por qué Lasso requiere escalado

Lasso intenta minimizar la suma de los errores al cuadrado más una penalización basada en el valor absoluto de los coeficientes ($\sum |w_i|$). Si una característica como `duration_ms` tiene valores en los millones, su coeficiente ($w$) será muy pequeño. Si otra como `speechiness` está entre 0 y 1, su coeficiente será grande. Lasso penalizaría más a `speechiness` simplemente por su escala, no por su importancia real. El **StandardScaler** elimina este sesgo.

#### 2. Interpretación del $R^2$ (R-cuadrado)

El valor que obtenemos con `pipeline.score()` nos indica qué proporción de la variabilidad del volumen (_loudness_) es explicada por nuestro modelo.

- Un $R^2$ cercano a **1** indica una predicción casi perfecta.
    
- Un $R^2$ cercano a **0** indica que el modelo no es mejor que predecir siempre el valor promedio.
    

#### 3. Ventaja de la Canalización

Al usar `Pipeline(steps)`, te aseguras de que:

- Se calculen la media y la desviación estándar **solo en `X_train`**.
    
- Esos mismos valores se usen para transformar `X_test`.
    
- Esto previene la **fuga de datos** (_data leakage_), un error crítico donde información del conjunto de prueba se "filtra" en el entrenamiento, dando resultados falsamente optimistas.
    

---

Este ejercicio representa la integración total de lo que hemos visto: **Escalado**, **Modelado**, **Validación Cruzada** y **Optimización**. Al usar una canalización para clasificar géneros musicales, garantizamos que el modelo sea robusto y que el parámetro de regularización $C$ sea el más adecuado para los datos ya normalizados.


```python
# Build the steps
# Definimos el escalador y el modelo de clasificación
steps = [("scaler", StandardScaler()),
         ("logreg", LogisticRegression())]
pipeline = Pipeline(steps)

# Create the parameter space
# Importante: usamos el nombre del paso 'logreg' + '__' + 'C'
parameters = {"logreg__C": np.linspace(0.001, 1.0, 20)}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=21)

# Instantiate the grid search object
# Pasamos la canalización completa y el espacio de parámetros
cv = GridSearchCV(pipeline, param_grid=parameters)

# Fit to the training data
cv.fit(X_train, y_train)

# Mostrar resultados
print(cv.best_score_, "\n", cv.best_params_)
```

---

### Análisis del Flujo de Trabajo Integrado

Como futuro **DevOps**, este tipo de estructuras son tus mejores amigas para la automatización de procesos de entrenamiento (CI/CD para ML). Aquí te explico los puntos clave:

#### 1. El Hiperparámetro $C$ en Regresión Logística

En `LogisticRegression`, el parámetro $C$ controla la **fuerza de la regularización** (es el inverso de $\lambda$ en Ridge/Lasso).

- Un **$C$ pequeño** (como $0.001$) impone una **regularización fuerte**, lo que simplifica el modelo para evitar el sobreajuste (_overfitting_).
    
- Un **$C$ grande** (cercano a $1.0$) impone una **regularización débil**, permitiendo que el modelo se ajuste más a los datos de entrenamiento.
    

#### 2. La sintaxis del doble guion bajo (`__`)

Cuando usas `GridSearchCV` con un `Pipeline`, Scikit-learn necesita saber a qué paso pertenece cada parámetro. La regla es:

`nombre_del_paso` + `__` + `nombre_del_parametro`.

En nuestro caso: `logreg__C`. Si intentas usar solo `C`, el sistema lanzará un error porque el Pipeline no tiene un atributo directo llamado $C$.

#### 3. Validación Cruzada con Escalado Correcto

Lo más potente de este código es que `GridSearchCV` realiza el escalado **dentro de cada pliegue (fold)** de la validación cruzada.

- **Paso 1:** Divide el conjunto de entrenamiento en 5 partes.
    
- **Paso 2:** Escala las 4 partes de entrenamiento y aplica esa misma transformación a la 1 parte de validación.
    
- **Paso 3:** Entrena el modelo.
    
    Esto evita que la media global de los datos se "filtre" en los resultados, dándote una métrica de `best_score_` extremadamente honesta.
    

---

### Nota de Ingeniería (Contexto DevOps/SysAdmin)

La capacidad de encontrar el mejor modelo automáticamente es lo que permite crear sistemas de auto-reentrenamiento. Si tu sistema detecta que el rendimiento baja (drifting), podrías disparar un job que ejecute este `GridSearchCV` para encontrar nuevos parámetros óptimos sin intervención humana.

