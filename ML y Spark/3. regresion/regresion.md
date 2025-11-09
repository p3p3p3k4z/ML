## Regresión Lineal en Spark ML

La regresión lineal es el modelo fundamental para la predicción de **valores numéricos**.

-----

### Concepto: Modelando la Tendencia

El objetivo de la regresión es encontrar una relación matemática (una línea recta en el caso más simple) que describa la **tendencia subyacente** en los datos. Queremos poder predecir un valor numérico continuo (ej. consumo de combustible) a partir de otras variables (ej. peso del auto, cilindros).

-----

### El Residuo: Midiendo el Error

Ningún modelo es perfecto; siempre habrá una diferencia entre lo que predice y la realidad.

  * **Definición:** El **residuo** es la diferencia entre el **valor real observado** ($y$) y el **valor predicho (modelado)** por el algoritmo ($\hat{y}$).
      * $Residuo = y - \hat{y}$
  * **Objetivo del Entrenamiento:** El "mejor" modelo es aquel que encuentra la línea que **minimiza** estos residuos en general.

-----

### Función de Pérdida (Loss Function)

Para "minimizar los residuos", necesitamos una forma de medirlos todos juntos. Esto es la **función de pérdida**.

  * **MSE (Mean Squared Error):** Es la función de pérdida más común. Toma cada residuo, lo eleva al cuadrado (para que todos sean positivos y penalizar más los errores grandes) y luego calcula el promedio.
      * $MSE = \frac{1}{N} \sum (y_i - \hat{y}_i)^2$

-----

### Construcción y Evaluación del Modelo en Spark

1.  **Entrenamiento:** Usamos `LinearRegression`. Al ajustar el modelo (`fit`), Spark encuentra los **coeficientes** (pesos) para cada predictor que minimizan el MSE.

    ```python
    from pyspark.ml.regression import LinearRegression
    # Crear y entrenar el modelo
    regression = LinearRegression(labelCol='consumption')
    regression_model = regression.fit(cars_train)
    ```

2.  **Examinar Coeficientes:** Podemos ver qué importancia le dio el modelo a cada variable.

      * Un coeficiente positivo significa que si esa variable aumenta, la predicción también aumenta.
      * Un coeficiente negativo significa una relación inversa.

3.  **Evaluación (RMSE):** Para saber qué tan bueno es el modelo, usamos métricas como el **RMSE (Root Mean Squared Error)**. Es la raíz cuadrada del MSE, lo que lo devuelve a las **mismas unidades** que la variable objetivo (ej. "el modelo se equivoca por 0.7 galones/milla en promedio").

    ```python
    from pyspark.ml.evaluation import RegressionEvaluator
    # Calcular RMSE en los datos de prueba
    evaluator = RegressionEvaluator(labelCol='consumption', metricName='rmse')
    rmse = evaluator.evaluate(predictions)
    ```