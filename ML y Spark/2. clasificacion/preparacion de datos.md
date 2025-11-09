La preparación y limpieza de datos es un paso fundamental antes de construir cualquier modelo de ML. En Spark, esto implica transformar el DataFrame para que sea adecuado para los algoritmos.

-----

### Selección y Limpieza de Columnas

El primer paso es **reducir los datos a lo necesario**. Esto significa **seleccionar los campos a conservar** o eliminar los que no son útiles (como identificadores únicos, nombres, etc.).

```python
# Opción 1: Eliminar las columnas que NO quieres
# .drop() elimina una o más columnas especificadas por nombre.
cars = cars.drop('maker', 'model')

# Opción 2: Seleccionar explícitamente las columnas que SÍ quieres conservar
# .select() crea un nuevo DataFrame solo con las columnas listadas.
cars = cars.select('origin', 'type', 'cyl', 'size', 'weight', 'length', 'rpm', 'consumption')
```

-----

### Filtrado de Datos Faltantes (Missing Data)

Los datos del mundo real suelen tener valores nulos (`null` o `NaN`). Es crucial manejarlos.

```python
# 1. Contar cuántos valores nulos hay en una columna específica ('cyl')
# .filter('cyl IS NULL') selecciona solo las filas donde 'cyl' es nulo.
nulos_cyl = cars.filter('cyl IS NULL').count()

# 2. Eliminar registros con valores nulos en una columna específica
# Mantenemos solo las filas donde 'cyl' NO ES NULO.
cars = cars.filter('cyl IS NOT NULL')

# 3. Eliminar registros con valores nulos en CUALQUIER columna
# .dropna() es un método directo para esto. Úsalo con precaución para no perder demasiados datos.
cars = cars.dropna()
```

-----

### Mutación de Columnas (Feature Engineering)

A menudo necesitamos crear nuevas columnas o transformar las existentes para que sean más útiles para el modelo (por ejemplo, convertir unidades).

```python
from pyspark.sql.functions import round

# Crear una nueva columna 'mass' (masa) a partir de 'weight' (peso en libras)
# Se divide por 2.205 para convertir a kg y se redondea a 0 decimales.
cars = cars.withColumn('mass', round(cars.weight / 2.205, 0))

# Convertir la columna 'length' (longitud) a metros
cars = cars.withColumn('length', round(cars.length * 0.0254, 3))
```

-----

### Indexación de Datos Categóricos

Los modelos de ML generalmente requieren entradas numéricas. Las columnas de texto (categóricas) deben convertirse a números.

  * **`StringIndexer`:** Es la herramienta de Spark MLlib para esto. Asigna un número (índice) a cada categoría única, generalmente basado en su frecuencia (la más común obtiene el índice 0.0).

<!-- end list -->

```python
from pyspark.ml.feature import StringIndexer

# Ejemplo 1: Indexar la columna 'type' (tipo de auto)
# inputCol: la columna de texto original.
# outputCol: el nombre de la nueva columna numérica que se creará.
indexer = StringIndexer(inputCol='type', outputCol='type_idx')

# Ajustar (fit) el indexador a los datos para que aprenda las categorías
indexer_model = indexer.fit(cars)

# Transformar los datos para crear la nueva columna
cars = indexer_model.transform(cars)

# Ejemplo 2: Indexar 'origin' (país de origen)
# Convertirá 'USA' a 0.0 y 'non-USA' a 1.0 (o viceversa, dependiendo de la frecuencia).
cars = StringIndexer(inputCol="origin", outputCol="label").fit(cars).transform(cars)
```

-----

### Ensamblaje de Vectores (VectorAssembler)

Este es un paso **único y crucial en Spark ML**.

  * **Requisito de Spark:** La mayoría de los algoritmos de ML en Spark esperan que **todas las características (features) de entrada estén consolidadas en una sola columna** de tipo vector.
  * **`VectorAssembler`:** Es el transformador que toma una lista de columnas (numéricas) y las combina en esta única columna de vectores.

<!-- end list -->

```python
from pyspark.ml.feature import VectorAssembler

# Definir qué columnas queremos usar como características del modelo
columnas_entrada = ['cyl', 'size', 'mass', 'length', 'rpm', 'consumption', 'type_idx']

# Crear el ensamblador
assembler = VectorAssembler(inputCols=columnas_entrada, outputCol='features')

# Transformar los datos. Ahora el DataFrame 'cars' tendrá una nueva columna 'features'
# que contiene un vector con todos los valores de las columnas de entrada para cada fila.
cars = assembler.transform(cars)
```