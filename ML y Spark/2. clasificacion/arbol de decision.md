## Árboles de Decisión en Spark ML

Un árbol de decisión es un modelo de ML versátil y fácil de interpretar que se usa tanto para clasificación como para regresión.

![arbol de decision](tree.png)
-----

### ¿Cómo se Construye? (Particionamiento Recursivo)

La idea central es dividir los datos repetidamente en grupos más pequeños y homogéneos basándose en las características más informativas.

1.  **Nodo Raíz:** Se comienza con **todos los registros** en el nodo superior.
2.  **Selección del Mejor Predictor:** El algoritmo evalúa todas las características (predictores) y elige la que mejor divide los datos en dos grupos lo más **puros** posible.
      * *Ejemplo:* Si queremos separar datos en dos clases (verde y azul), una buena división sería aquella donde un grupo resultante tenga mayoritariamente registros "verdes" y el otro "azules".
3.  **División (Splitting):** Los datos se dividen según esa regla.
4.  **Recursión:** El proceso **se repite** para cada nuevo subgrupo (nodo secundario) hasta que se cumple un criterio de parada (ej. el nodo es puro o se alcanzó la profundidad máxima).

-----

### Clasificación con Árboles de Decisión

En una tarea de clasificación, el objetivo es predecir una categoría.

  * **Etiquetado de Nodos:** Cada nodo final (hoja) se etiqueta con la **clase predominante** de los registros que cayeron en él. Por ejemplo, si en una hoja hay 10 registros "verdes" y 2 "azules", cualquier nuevo dato que caiga ahí será clasificado como "verde".

#### Ejemplo Práctico: Clasificar Autos

Queremos predecir si un auto fue fabricado en "USA" o "fuera de USA" (non-USA) basándonos en sus características (cilindros, peso, etc.).

1.  **Preparación:** Primero, dividimos los datos en conjunto de entrenamiento (80%) y prueba (20%) para poder evaluar después.
    ```python
    # Dividir datos en entrenamiento (80%) y prueba (20%)
    # seed=23 asegura que la división sea reproducible.
    cars_train, cars_test = cars.randomSplit([0.8, 0.2], seed=23)
    ```
2.  **Entrenamiento:** Creamos un `DecisionTreeClassifier` y lo ajustamos (`fit`) a los datos de entrenamiento.
    ```python
    from pyspark.ml.classification import DecisionTreeClassifier

    # Crear el clasificador (sin configurar hiperparámetros por ahora)
    tree = DecisionTreeClassifier()

    # Entrenar el modelo con los datos de entrenamiento
    tree_model = tree.fit(cars_train)
    ```

-----

### Evaluación del Modelo

Una vez entrenado, debemos probar que funcione correctamente usando datos que no ha visto (el conjunto de prueba).

1.  **Predicción:** Usamos el modelo para generar predicciones sobre el conjunto de prueba.
    ```python
    # Generar predicciones en los datos de prueba
    prediction = tree_model.transform(cars_test)
    ```
2.  **Matriz de Confusión:** Es una excelente herramienta para entender el rendimiento detallado, más allá de la simple exactitud. Muestra cuántos verdaderos positivos (TP), falsos positivos (FP), etc., tuvo el modelo.
    ```python
    # Mostrar la matriz de confusión agrupando por la etiqueta real y la predicción
    prediction.groupBy("label", "prediction").count().show()
    ```

Esta matriz nos permite ver exactamente dónde se está equivocando el modelo (ej. ¿está confundiendo muchos autos de USA como si fueran de fuera?).