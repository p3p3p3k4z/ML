## Validación Cruzada (Cross-Validation) en Spark ML

La validación cruzada es una técnica esencial para evaluar la robustez de un modelo de ML y para ajustar sus hiperparámetros de manera confiable.

-----

### El Problema: Limitaciones de una sola división

El enfoque más simple es dividir los datos aleatoriamente en un conjunto de entrenamiento y uno de prueba.

  * **Inconveniente:** Solo obtienes una única estimación del rendimiento. Si por casualidad el conjunto de prueba fue "fácil" o "difícil", tu estimación podría ser engañosa.
  * **Idea:** ¿Qué pasaría si pudiéramos probar el modelo varias veces con diferentes divisiones de datos para tener una idea más sólida de su rendimiento real?

-----

### La Solución: K-Fold Cross-Validation 🔄

La validación cruzada de K pliegues (*K-Fold Cross-Validation*) es el método estándar.

1.  **División Inicial:** Comienza con el conjunto de datos de entrenamiento completo (es importante aleatorizarlo primero).
2.  **Particiones (Folds):** Divide estos datos en $K$ particiones (o *folds*) de igual tamaño. El número $K$ influye en el nombre (ej. 10-fold CV).
3.  **Proceso Iterativo:**
      * En la iteración 1: Usa el **Fold 1 como validación** y los Folds 2 a $K$ para entrenar. Evalúa y guarda la métrica.
      * En la iteración 2: Usa el **Fold 2 como validación** y el resto para entrenar. Evalúa y guarda la métrica.
      * ... Repite $K$ veces.
4.  **Resultado Final:** El rendimiento del modelo es el **promedio** de las métricas obtenidas en las $K$ iteraciones.

-----

### Ajuste de Hiperparámetros (Grid Search)

La validación cruzada brilla realmente cuando queremos encontrar la mejor combinación de hiperparámetros (ej. los valores de `regParam` y `elasticNetParam` en una regresión).

  * **Grid Search:** Definimos una "cuadrícula" de posibles valores para cada parámetro.
  * **Proceso:** Para *cada* combinación de parámetros en la cuadrícula, ejecutamos todo el proceso de validación cruzada.
  * **Selección:** El modelo final es el que tuvo el mejor rendimiento promedio en la validación cruzada.

-----

### Implementación en Spark ML

En Spark, usamos `CrossValidator` junto con `ParamGridBuilder`.

1.  **Definir la Cuadrícula de Parámetros:**

    ```python
    from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

    # Construir la cuadrícula de hiperparámetros a probar
    # Ej: probaremos regParam=0.01, 0.1, 1.0 y elasticNetParam=0.0, 0.5, 1.0
    # Esto resulta en 3 x 3 = 9 combinaciones a probar.
    params = ParamGridBuilder() \
        .addGrid(regression.regParam, [0.01, 0.1, 1.0]) \
        .addGrid(regression.elasticNetParam, [0.0, 0.5, 1.0]) \
        .build()
    ```

2.  **Configurar el CrossValidator:**
    Necesita saber qué estimador usar (tu modelo o pipeline), qué parámetros probar (la cuadrícula) y cómo evaluar cada intento (un evaluador).

    ```python
    # Crear el validador cruzado
    # numFolds=10 es un valor común (pero costoso computacionalmente).
    cv = CrossValidator(estimator=regression, # O tu 'pipeline' completo
                        estimatorParamMaps=params,
                        evaluator=evaluator, # Ej: RegressionEvaluator con RMSE
                        numFolds=10,
                        seed=13) # Semilla para reproducibilidad en la división de folds
    ```

3.  **Entrenar (y esperar...):**
    El `CrossValidator` actúa como un estimador. Al llamar a `.fit()`, ejecuta todas las combinaciones y folds. ¡Esto puede tardar mucho\!

    ```python
    # Entrena los 9 modelos x 10 folds = 90 entrenamientos en total.
    cv_model = cv.fit(cars_train)
    ```

4.  **Mejor Modelo:**
    El objeto `cv_model` resultante se comporta como el mejor modelo encontrado. Puedes usarlo directamente para hacer predicciones.

    ```python
    # Usar el mejor modelo para predecir en el conjunto de prueba REAL (final)
    predictions = cv_model.transform(cars_test)

    # Ver el rendimiento promedio del mejor modelo durante la validación cruzada
    print(max(cv_model.avgMetrics)) # O min() si la métrica es de error como RMSE
    ```