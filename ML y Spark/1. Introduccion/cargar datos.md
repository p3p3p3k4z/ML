## Carga de Datos en Spark

En Spark, la forma moderna de trabajar con datos es mediante **DataFrames**.

-----

### El DataFrame: Representación de Datos

  * **Definición:** Un DataFrame es una colección distribuida de datos organizados en columnas con nombre. Es conceptualmente equivalente a una tabla en una base de datos relacional o a un DataFrame en pandas/R, pero con optimizaciones internas para trabajar a gran escala.
  * **Estructura:**
      * Los datos se capturan en **filas** (registros).
      * Cada fila se divide en **columnas** (campos).
      * Cada columna tiene un **nombre** y un **tipo de dato** específico (string, integer, double, etc.).

-----

### Carga desde Archivos CSV

El formato **CSV (Comma-Separated Values)** es uno de los más comunes para almacenar datos tabulares. Spark facilita su lectura directa a un DataFrame.

```python
# Carga básica de un archivo CSV
# header=True: Indica que la primera fila contiene los nombres de las columnas.
# inferSchema=True: Spark intenta adivinar automáticamente los tipos de datos (ej. números vs. texto).
df = spark.read.csv('datos.csv', header=True, inferSchema=True)
```

#### Argumentos Opcionales Comunes para `.csv()`:

  * `header` (default: `False`): ¿La primera fila es un encabezado?
  * `sep` (default: `,`): El separador de campos (puede ser `;`, `|`, tabulador `\t`, etc.).
  * `inferSchema` (default: `False`): Si es `True`, Spark recorre el archivo para deducir los tipos de datos. Si es `False`, todas las columnas se cargan como texto (string).
  * `nullValue`: Permite especificar qué cadena de caracteres en el archivo debe interpretarse como un valor nulo (`null`).

-----

### Métodos y Atributos Esenciales del DataFrame

Una vez cargados los datos en un DataFrame (`df`), usamos estos métodos para inspeccionarlos:

  * `.count()`: Devuelve el **número total de filas** en el DataFrame.
  * `.show(n)`: Muestra las primeras `n` filas del DataFrame en formato tabular (por defecto `n=20`). Útil para una vista rápida.
  * `.printSchema()`: Imprime la estructura del DataFrame en forma de árbol, mostrando el **nombre de cada columna y su tipo de dato**.
  * `.dtypes`: Devuelve una lista de tuplas `(nombre_columna, tipo_dato)`, similar a `.printSchema()` pero programáticamente accesible.