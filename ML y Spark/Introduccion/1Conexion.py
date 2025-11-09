# 1. Importa la clase SparkSession de pyspark.sql
from pyspark.sql import SparkSession

# 2. Crea un objeto SparkSession conectado a un clúster local
#    - master("local[*]"): Utiliza todos los núcleos disponibles.
#    - appName('test'): Nombra la aplicación 'test'.
#    - getOrCreate(): Obtiene la sesión existente o crea una nueva si no existe.
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("test") \
    .getOrCreate()

# 3. Recuperar la versión de Spark
#    - Se utiliza el atributo 'version' del objeto SparkSession.
spark_version = spark.version
print(f"La versión de Spark ejecutándose en el clúster es: {spark_version}")

# 4. Apagar el clúster (detener la SparkSession)
spark.stop()