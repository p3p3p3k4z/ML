El objetivo es construir un modelo de **regresión lineal múltiple** para predecir las ventas (`sales`) utilizando tres canales de inversión publicitaria: `tv`, `radio` y `social_media`.

Trabajaremos con el DataFrame `sales_df`, dividiremos los datos en conjuntos de entrenamiento (70%) y prueba (30%), e instanciaremos el algoritmo `LinearRegression` de scikit-learn para realizar las predicciones.


```python
# Create X and y arrays
# .drop elimina la columna objetivo para dejar solo las características
# .values convierte el DataFrame/Series de pandas en arreglos NumPy
X = sales_df.drop("sales", axis=1).values
y = sales_df["sales"].values

# Dividimos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Instantiate the model
reg = LinearRegression()

# Fit the model to the data (Aprendizaje de coeficientes a y b)
reg.fit(X_train, y_train)

# Make predictions utilizando los datos que el modelo NO ha visto
y_pred = reg.predict(X_test)

print("Predictions: {}, Actual Values: {}".format(y_pred[:2], y_test[:2]))
```

---

### **Explicación Paso a Paso**

1. **Preparación de X e y:** * `X` debe ser una matriz (bidimensional). Usamos `.drop("sales", axis=1)` para tomar todas las columnas excepto la que queremos predecir.
    
    - `y` es nuestro vector objetivo. Usamos `.values` porque scikit-learn prefiere trabajar con arreglos de NumPy para optimizar el rendimiento matemático (especialmente importante en tu CPU, ya que NumPy maneja operaciones vectoriales de forma eficiente).
        
2. **`train_test_split`:** * Es la "regla de oro" del Machine Learning. Si entrenas con todos los datos, no sabrás si tu modelo realmente aprendió o si simplemente memorizó los datos (overfitting). Al separar un 30% para prueba, evaluamos al modelo con "preguntas nuevas".
    
3. **`reg.fit(X_train, y_train)`:** * Aquí es donde ocurre la magia del **Mínimos Cuadrados Ordinarios (OLS)**. El algoritmo calcula los coeficientes para `tv`, `radio` y `social_media` que minimizan la suma de los cuadrados de los residuos.
    
4. **`reg.predict(X_test)`:** * Una vez que el modelo conoce la pendiente y el intercepto, le pasamos los datos de prueba para ver qué ventas estima.
    

---

### **Complementos Técnicos**

#### **La importancia de la dimensionalidad**

En la regresión simple, ajustamos una **línea**. En este ejercicio, al tener 3 características (`tv`, `radio`, `social_media`), estamos ajustando un **hiperplano** en un espacio de 4 dimensiones. Aunque no podemos visualizarlo fácilmente, la lógica matemática es idéntica: minimizar la distancia vertical de los puntos al plano.

#### **¿Qué pasa internamente en los coeficientes?**

Después de ejecutar el código, podrías inspeccionar qué canal de publicidad es más efectivo usando:

- `reg.coef_`: Te dirá cuánto aumentan las ventas por cada dólar invertido en cada red.
    
- `reg.intercept_`: Te dirá el nivel de ventas base si la inversión en publicidad fuera cero.

---
## Rendimiento de Regresion
Tras haber ajustado un modelo de regresión utilizando las características de inversión publicitaria y haber generado predicciones, el paso crítico es evaluar su desempeño mediante métricas estadísticas. En este ejercicio, el objetivo es cuantificar qué proporción de la varianza de las ventas puede ser explicada por el modelo (utilizando el coeficiente de determinación $R^2$) y determinar la magnitud del error promedio en las predicciones sobre datos no vistos (utilizando la Raíz del Error Cuadrático Medio o RMSE).

Ahora que has ajustado un modelo `reg` utilizando todas las características de `sales_df` y has hecho predicciones de los valores de las ventas, puedes evaluar el rendimiento utilizando algunas métricas de regresión habituales.

Se han precargado las variables `X_train`, `X_test`, `y_train`, `y_test` e `y_pred`, junto con el modelo ajustado, `reg`, todas del último ejercicio.

Tu tarea consiste en averiguar lo bien que las características pueden explicar la varianza de los valores objetivo, además de evaluar la capacidad del modelo para hacer predicciones sobre datos no vistos.


```python
# Importar root_mean_squared_error desde sklearn.metrics
from sklearn.metrics import root_mean_squared_error

# Calcular la puntuación R-cuadrado (R^2)
# El método .score() en regresión devuelve el coeficiente de determinación
r_squared = reg.score(X_test, y_test)

# Calcular el error cuadrático medio (RMSE)
# Comparamos las etiquetas reales (y_test) con las predicciones (y_pred)
rmse = root_mean_squared_error(y_test, y_pred)

# Imprimir las métricas para su análisis
print("R^2: {}".format(r_squared))
print("RMSE: {}".format(rmse))
```

---

### Análisis de las Métricas de Rendimiento

Para determinar si un modelo de regresión es "bueno", no basta con observar una línea; necesitamos números que validen su capacidad de generalización.

#### El Coeficiente de Determinación ($R^2$)

Esta métrica indica qué porcentaje de la variabilidad de la variable objetivo es explicada por las características del modelo.

- **Escala:** Generalmente va de **0 a 1**.
    
- **Interpretación:** Un $R^2$ de 0.85 significa que el 85% de la variación en las ventas se puede explicar por el gasto en publicidad. Entre más cerca esté de 1, mejor "encaja" el modelo con los datos.
    
- **Nota técnica:** Si el $R^2$ es muy bajo, es posible que la relación entre las variables no sea lineal o que falten características importantes.
    

#### Raíz del Error Cuadrático Medio (RMSE)

Mientras que el $R^2$ nos habla de proporción, el RMSE nos habla de **error absoluto en las mismas unidades que la variable objetivo**.

- **Cálculo:** Se basa en el Error Cuadrático Medio ($MSE$), que promedia los cuadrados de las diferencias entre el valor real y el predicho:
    
    $$MSE = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$
    
- **RMSE:** Al aplicar la raíz cuadrada al MSE ($RMSE = \sqrt{MSE}$), obtenemos un valor que podemos interpretar directamente. Si el RMSE es 500, significa que, en promedio, las predicciones del modelo se desvían **$500** de las ventas reales.
    

---

**Diferencia clave entre métricas:**

- **$R^2$** es una métrica **relativa** (te dice qué tan bien se ajusta la tendencia).
    
- **RMSE** es una métrica **absoluta** (te dice cuánto dinero estás fallando en promedio).

---
