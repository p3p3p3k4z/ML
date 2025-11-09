## Regresión Logística en Spark ML

La regresión logística es un modelo fundamental de **clasificación** (a pesar de su nombre "regresión"). Se utiliza para predecir la probabilidad de que una observación pertenezca a una de dos clases (clasificación binaria).

-----

### Concepto Clave: La Función Logística (Sigmoide)

A diferencia de la regresión lineal que predice un valor continuo (ej. precio), la regresión logística modela una **probabilidad** entre 0 y 1.

  * **Función Sigmoide:** Transforma cualquier valor de entrada (una combinación lineal de los predictores) en un valor entre 0 y 1. Su forma es una curva en "S".
  * **Umbral (Threshold):** Para tomar una decisión final (clasificar como 0 o 1), se establece un umbral, típicamente en **0.5**.
      * Si la probabilidad predicha es $> 0.5$ $\rightarrow$ Clase 1 (Verdadero).
      * Si la probabilidad predicha es $\leq 0.5$ $\rightarrow$ Clase 0 (Falso).

-----

### Entrenamiento del Modelo

El objetivo del entrenamiento es encontrar los mejores coeficientes (pesos) para las variables predictoras.

  * **Curva y Coeficientes:** Los coeficientes determinan la forma y posición de la curva sigmoide.
      * **Desplazamiento:** Un coeficiente puede desplazar la curva hacia la izquierda o derecha.
      * **Pendiente:** Otro coeficiente puede hacer que la transición entre clases (la parte inclinada de la "S") sea más **gradual o más rápida**.
  * **En Spark:** Usamos `LogisticRegression` de `pyspark.ml.classification`.

<!-- end list -->

```python
from pyspark.ml.classification import LogisticRegression

# Crear el clasificador
logistic = LogisticRegression()

# Entrenar con los datos de entrenamiento
# Spark encuentra los coeficientes óptimos aquí.
logistic_model = logistic.fit(cars_train)
```

-----

### Evaluación: Más allá de la Exactitud

Para evaluar modelos de clasificación, especialmente si las clases están desbalanceadas, necesitamos métricas más detalladas que la simple exactitud.

#### 1\. Precisión, Recall y Métricas Ponderadas

  * **Precisión:** De los que predije positivos, ¿cuántos lo eran realmente? (Evitar falsos positivos).
  * **Recall (Sensibilidad):** De todos los positivos reales, ¿cuántos detecté? (Evitar falsos negativos).
  * **Métricas Ponderadas (Weighted):** Si tienes muchas más observaciones de una clase que de otra, el promedio simple puede ser engañoso. Las métricas ponderadas tienen en cuenta el número de observaciones de cada clase.

<!-- end list -->

```python
# Evaluación con métricas ponderadas en Spark
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator()
weighted_precision = evaluator.evaluate(prediction, {evaluator.metricName: "weightedPrecision"})
```

#### 2\. Curva ROC y AUC

Son herramientas estándar para evaluar clasificadores binarios, independientemente del umbral elegido.

  * **Curva ROC (Receiver Operating Characteristic):** Gráfica que muestra el rendimiento del modelo en todos los umbrales de clasificación posibles. Compara la tasa de Verdaderos Positivos (TPR) contra la tasa de Falsos Positivos (FPR).
  * **AUC (Area Under the Curve):** Es un número único que resume la curva ROC.
      * **AUC = 0.5:** El modelo es tan bueno como lanzar una moneda (aleatorio).
      * **AUC = 1.0:** Modelo perfecto.
      * Cuanto más cerca de 1, mejor es el modelo separando las clases.
