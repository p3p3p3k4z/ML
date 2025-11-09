## Conexión a Spark: La SparkSession

El punto de entrada unificado para cualquier aplicación de Spark es la `SparkSession`. Es el objeto que coordina todo el trabajo.

-----

### La Conexión (El Programa Controlador)

**La conexión a Spark la establece el programa controlador (Driver)**. Este es el programa principal (tu script o *notebook*) que define el flujo de la aplicación.

  * **Lenguajes:** Este programa puede estar escrito en **Java, Scala, Python (PySpark) o R**.
  * **Comparación:**
      * **Java** es considerado **verboso** y, a menudo, requiere más código para tareas simples.
      * **Scala, Python y R** son lenguajes de **alto nivel** que permiten escribir **poco código**.
  * **REPL:** Estos lenguajes de alto nivel también ofrecen un **REPL (Bucle Lectura-Evaluación-Impresión)**, que es **crucial para el desarrollo interactivo** y el análisis exploratorio de datos.

-----

### Creación de la SparkSession (Ejemplo PySpark)

Para crear la sesión, se utiliza un patrón de diseño *Builder*.

```python
# 1. Importar la biblioteca necesaria
from pyspark.sql import SparkSession

# 2. Construir la sesión usando el patrón Builder
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("first_spark_application") \
    .getOrCreate()

# ... Aquí va tu código para interactuar con Spark ...

# 3. Cerrar la conexión al finalizar
spark.stop()
```

  * `SparkSession.builder`: Inicia el constructor.
  * `.master(...)`: Especifica a qué clúster conectarse.
  * `.appName(...)`: Le da un nombre a tu aplicación (útil para monitorear la UI de Spark).
  * `.getOrCreate()`: Obtiene la `SparkSession` activa si ya existe una, o crea una nueva si no.

-----

### ¿Dónde está el Clúster? (El método `.master()`)

El método `.master()` le dice a Spark cómo y dónde ejecutar el trabajo:

  * **Clúster Local (para desarrollo):**
      * `master("local")`: Ejecuta Spark en un solo hilo (sin paralelismo).
      * `master("local[4]")`: Ejecuta Spark localmente usando 4 núcleos.
      * `master("local[*]")`: (El más común para desarrollo) Ejecuta Spark localmente usando todos los núcleos de CPU disponibles en tu máquina.
  * **Clúster Remoto (para producción):**
      * Para **conectar a un clúster remoto** (como YARN, Mesos o un clúster Standalone), aquí se proporciona la **URL de Spark** o el identificador del administrador de recursos (ej. `yarn`).

-----

### El Ecosistema Moderno: DataFrames

La `SparkSession` es la puerta de entrada a la API de **DataFrames**. Es importante notar que existen dos versiones de las bibliotecas ML de Spark:

  * `spark.mllib`: La API original basada en **RDDs (Resilient Distributed Datasets)**. Esta **representación no estructurada de datos ha quedado obsoleta**.
  * `spark.ml`: La API moderna que **se basa en una representación tabular y estructurada de datos en DataFrames**. Esta es la biblioteca estándar que se debe utilizar hoy en día.