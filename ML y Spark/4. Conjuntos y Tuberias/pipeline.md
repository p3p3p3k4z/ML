## Pipelines en Spark ML: Agilizando el Flujo de Trabajo 🚀

Construir un modelo de Machine Learning rara vez es un solo paso. Implica una secuencia de tareas de preparación de datos, ingeniería de características y, finalmente, el entrenamiento del modelo.

Un **Pipeline** (tubería o canalización) es un mecanismo que nos permite **combinar y encadenar** todos estos pasos en una sola unidad de trabajo.

-----

### El Problema: Fuga de Información (Data Leakage) 💧

Uno de los errores más graves y comunes en ML es la **fuga de información**. Ocurre cuando información del conjunto de prueba (que debería ser "invisible" para el modelo durante el entrenamiento) se filtra accidentalmente en el proceso de entrenamiento.

  * **Causa Común:** Aplicar transformaciones que "aprenden" de los datos (como `StringIndexer` o la normalización) a **todo el conjunto de datos antes de dividirlo**, o aplicar el método `.fit()` incorrectamente a los datos de prueba.
  * **Consecuencia:** El modelo parece tener un rendimiento espectacular durante el desarrollo, pero falla estrepitosamente en producción porque "hizo trampa" durante la evaluación.
  * **Regla de Oro:** Para tener resultados sólidos, el método `.fit()` (que aprende parámetros de los datos) debe aplicarse **ÚNICAMENTE a los datos de entrenamiento**. El método `.transform()` se aplica tanto a entrenamiento como a prueba.

-----

### La Solución: Pipelines

Los Pipelines solucionan este problema y simplifican enormemente el código al encapsular todo el flujo.

  * **Concepto:** En lugar de aplicar cada paso (indexar, codificar, ensamblar, entrenar) individualmente y gestionar manualmente qué datos van a dónde, agrupamos todos los pasos en un objeto `Pipeline` y lo ejecutamos como una sola unidad.
  * **Componentes de un Pipeline:**
      * **Transformadores (`Transformer`):** Algoritmos que transforman un DataFrame en otro (ej. `OneHotEncoder`, `VectorAssembler`, o un modelo ya entrenado). Tienen un método `.transform()`.
      * **Estimadores (`Estimator`):** Algoritmos que se ajustan a los datos para producir un Transformador (ej. `StringIndexer`, `LinearRegression`). Tienen un método `.fit()`.

-----

### Implementación en Spark

Un Pipeline se define como una secuencia de etapas (`stages`).

1.  **Definir las etapas individuales:**

    ```python
    from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
    from pyspark.ml.regression import LinearRegression

    # Etapa 1: Indexar la columna 'type'
    indexer = StringIndexer(inputCol='type', outputCol='type_idx')

    # Etapa 2: One-hot encoding
    onehot = OneHotEncoder(inputCols=['type_idx'], outputCols=['type_dummy'])

    # Etapa 3: Ensamblar todas las características en un vector
    assemble = VectorAssembler(inputCols=['mass', 'cyl', 'type_dummy'], outputCol='features')

    # Etapa 4: El modelo de regresión
    regression = LinearRegression(labelCol='consumption')
    ```

2.  **Crear el Pipeline:**
    Unimos las etapas en el orden correcto.

    ```python
    from pyspark.ml import Pipeline

    # Crear el pipeline con la lista de etapas ordenadas
    pipeline = Pipeline(stages=[indexer, onehot, assemble, regression])
    ```

3.  **Entrenar y Usar el Pipeline:**

      * Al llamar a `pipeline.fit(training_data)`, Spark ejecuta automáticamente `.fit()` y `.transform()` en secuencia para todas las etapas usando **solo los datos de entrenamiento**. Esto garantiza que no haya fugas.
      * El resultado es un `PipelineModel` que sabe cómo realizar todos los pasos de transformación y predicción.
      * Para hacer predicciones, simplemente llamamos a `pipeline_model.transform(test_data)`.

    <!-- end list -->

    ```python
    # Entrenar todo el flujo de una sola vez
    pipeline_model = pipeline.fit(cars_train)

    # Hacer predicciones en datos nuevos automáticamente
    predictions = pipeline_model.transform(cars_test)
    ```

-----

### Acceso a las Etapas Internas

Si necesitas inspeccionar una parte específica del modelo entrenado (por ejemplo, para ver los coeficientes de la regresión lineal), puedes acceder a las etapas individuales del `PipelineModel` usando su índice.

```python
# Acceder a la etapa 3 (que es LinearRegression, índice 3 porque empezamos en 0)
regression_model = pipeline_model.stages[3]

# Ver el intercepto y los coeficientes
print(regression_model.intercept)
print(regression_model.coefficients)
```
