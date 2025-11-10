## Grid Search: Ajuste de Hiperparámetros en Spark ML 🎯

El **ajuste de hiperparámetros** es el proceso de encontrar la mejor configuración para un modelo de Machine Learning antes de comenzar el entrenamiento. El rendimiento del modelo puede mejorar drásticamente con los parámetros correctos.

-----

### El Problema: ¿Qué parámetros elegir?

Cada algoritmo de ML tiene "perillas" que podemos ajustar. Por ejemplo, en una regresión lineal regularizada, tenemos:

  * `fitIntercept`: ¿Debería el modelo calcular una intersección (ordenada al origen)?
  * `regParam` ($\lambda$): ¿Qué tan fuerte debe ser la regularización?
  * `elasticNetParam` ($\alpha$): ¿Qué tipo de regularización usar (Ridge, Lasso, ElasticNet)?

Probar manualmente cada combinación es tedioso y propenso a errores. Además, usar una **única estimación del RMSE** (división simple train/test) para comparar estas combinaciones no es muy sólido, ya que podría depender de la suerte de esa división específica.

-----

### La Solución: Grid Search con Cross-Validation 🔎

La **Búsqueda en Cuadrícula (Grid Search)** es una técnica sistemática para probar múltiples combinaciones de parámetros.

  * **Concepto:** Definimos una "cuadrícula" de valores posibles para cada parámetro. El algoritmo prueba *todas* las combinaciones posibles de estos valores.
  * **Evaluación Robusta:** Para cada combinación, se construye y evalúa un modelo utilizando **Validación Cruzada (Cross-Validation)**. Esto nos da una estimación mucho más confiable de qué tan bien funcionará esa configuración en la realidad.
  * **Selección:** Al final, elegimos la combinación de parámetros que tuvo el mejor rendimiento promedio en la validación cruzada.

-----

### Implementación en Spark ML

En Spark, usamos `ParamGridBuilder` para definir la cuadrícula y `CrossValidator` para ejecutar la búsqueda.

#### 1\. Construir la Cuadrícula de Parámetros (`ParamGridBuilder`)

Definimos qué parámetros y qué valores queremos probar.

```python
from pyspark.ml.tuning import ParamGridBuilder

# Supongamos que tenemos un modelo 'regression' (LinearRegression)
# Queremos probar:
# - fitIntercept: True o False (2 valores)
# - regParam: 0.001, 0.01, 0.1, 1.0, 10.0 (5 valores)
# - elasticNetParam: 0.0, 0.25, 0.5, 0.75, 1.0 (5 valores)

params = ParamGridBuilder() \
    .addGrid(regression.fitIntercept, [True, False]) \
    .addGrid(regression.regParam, [0.001, 0.01, 0.1, 1.0, 10.0]) \
    .addGrid(regression.elasticNetParam, [0.0, 0.25, 0.5, 0.75, 1.0]) \
    .build()

# Total de modelos a probar: 2 * 5 * 5 = 50 combinaciones.
print('Número de modelos a probar:', len(params))
```

#### 2\. Ejecutar la Búsqueda con `CrossValidator`

Configuramos el `CrossValidator` con el estimador (modelo o pipeline), la cuadrícula (`params`) y el evaluador.

```python
from pyspark.ml.tuning import CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator

# Crear el evaluador (RMSE)
evaluator = RegressionEvaluator(labelCol='consumption', metricName='rmse')

# Crear el CrossValidator
# numFolds=10 significa que para CADA una de las 50 combinaciones,
# se entrenarán 10 modelos (uno por fold). Total = 500 entrenamientos.
cv = CrossValidator(estimator=regression,
                    estimatorParamMaps=params,
                    evaluator=evaluator,
                    numFolds=10,
                    seed=13)

# Ejecutar la búsqueda (¡esto puede tardar!)
cv_model = cv.fit(cars_train)
```

#### 3\. El Mejor Modelo y sus Parámetros

Una vez que termina `.fit()`, el objeto resultante `cv_model` es el **mejor modelo** encontrado, ya re-entrenado con todos los datos de entrenamiento usando los mejores parámetros.

  * **Usar el mejor modelo:**

    ```python
    # Hacer predicciones directamente con el mejor modelo
    predictions = cv_model.transform(cars_test)
    ```

  * **Inspeccionar los mejores parámetros:**
    Podemos acceder al mejor modelo subyacente y ver qué parámetros ganaron.

    ```python
    # Acceder al mejor modelo
    best_model = cv_model.bestModel

    # Ver un parámetro específico (ej. fitIntercept)
    print(best_model.getOrDefault('fitIntercept'))

    # O ver todos los parámetros explicados
    # print(best_model.explainParams())
    ```

El Grid Search con Cross-Validation es el estándar de oro para ajustar modelos, asegurando que hemos explorado sistemáticamente las opciones y elegido la configuración más robusta.