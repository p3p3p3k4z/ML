# Ingeniería de Características (Feature Engineering) en Spark ML

La **ingeniería de características** es el arte de transformar los datos brutos en "características" (features) que representan mejor el problema subyacente para los modelos predictivos. A menudo, las mejoras de rendimiento más significativas no vienen de elegir un algoritmo diferente, sino de una **manipulación cuidadosa de las características**.

-----

### Bucketing (Discretización) 🗑️

A veces, una variable continua (como la edad, la altura o las RPM de un motor) no tiene una relación lineal simple con lo que queremos predecir. Puede ser más útil agrupar estos valores continuos en categorías discretas o "contenedores" (*buckets* o *bins*).

  * **Concepto:** Convertir una variable continua en una variable discreta (categórica) asignando valores a contenedores basados en rangos definidos por **límites (splits)**.
  * **Tipos de Contenedores:**
      * **Ancho uniforme:** Cada contenedor cubre el mismo rango de valores (ej. 0-10, 10-20, 20-30).
      * **Ancho variable:** Los rangos se definen manualmente según el conocimiento del dominio (ej. rangos de RPM específicos donde el motor se comporta diferente).

#### Implementación en Spark: `Bucketizer`

En Spark, usamos `Bucketizer` para esta tarea.

1.  **Definir los límites (splits):** Debemos especificar los puntos de corte.

    ```python
    from pyspark.ml.feature import Bucketizer

    # Definir los límites de los contenedores
    # Contenedor 0: [3500, 4500)
    # Contenedor 1: [4500, 6000)
    # Contenedor 2: [6000, 6500]
    splits = [3500, 4500, 6000, 6500]

    # Crear el Bucketizer
    bucketizer = Bucketizer(splits=splits,
                            inputCol="rpm",
                            outputCol="rpm_bin")
    ```

2.  **Transformar:** Al aplicar el `Bucketizer`, obtenemos una nueva columna con el índice del contenedor (0.0, 1.0, 2.0, etc.).

    ```python
    # Aplicar la transformación a los datos
    bucketed = bucketizer.transform(cars)

    # Ver los resultados
    bucketed.select('rpm', 'rpm_bin').show(5)
    ```

3.  **Uso posterior:** A menudo, estas nuevas variables discretas se convierten luego en variables *dummy* usando **One-Hot Encoding**, lo que permite al modelo aprender un coeficiente diferente para cada rango de valores.

-----

### Otras Operaciones de Ingeniería 🛠️

Además del bucketing, la ingeniería de características incluye muchas otras transformaciones matemáticas para revelar relaciones ocultas.

  * **Operaciones en una sola columna:**

      * **Logaritmo (`log()`):** Muy útil para manejar datos con distribuciones sesgadas (como ingresos o precios), comprimiendo los valores grandes.
      * **Raíz cuadrada (`sqrt()`), Potencia (`pow()`):** Para modelar relaciones no lineales.

  * **Operaciones entre dos o más columnas:**

      * **Producto:** Multiplicar dos variables para capturar su interacción.
      * **Ratio (Cociente):** Dividir una variable por otra para crear una nueva tasa o densidad.
          * *Ejemplo:* Crear una característica de "densidad" dividiendo la masa por la longitud (densidad lineal), por el área (densidad superficial) o por el volumen.

    <!-- end list -->

    ```python
    # Ejemplos de creación de nuevas características de densidad
    # Densidad lineal = masa / longitud
    cars = cars.withColumn('density_line', cars.mass / cars.length)

    # Densidad de área = masa / longitud^2
    cars = cars.withColumn('density_quad', cars.mass / cars.length**2)

    # Densidad de volumen = masa / longitud^3
    cars = cars.withColumn('density_cube', cars.mass / cars.length**3)
    ```

Estas nuevas características creadas a partir del conocimiento del dominio a menudo son mucho más predictivas que las variables originales por sí solas.