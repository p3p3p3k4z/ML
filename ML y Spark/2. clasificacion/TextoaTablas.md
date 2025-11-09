## Procesamiento de Lenguaje Natural (NLP): De Texto a Tablas en Spark ML

En el Machine Learning, la gran mayoría del trabajo (a menudo se dice que el **80%**) es la **preparación de datos**. Esto es especialmente cierto cuando trabajamos con texto, que es inherentemente **no estructurado**.

Antes de poder usar algoritmos de ML, debemos transformar este texto "crudo" (emails, SMS, libros) en una **estructura tabular** numérica que la máquina pueda entender.

-----

### El Proceso de Conversión: Paso a Paso

El objetivo final es crear una **matriz término-documento**, donde cada fila es un documento y cada columna representa una palabra (o término), indicando su frecuencia o importancia.

#### 1\. Tokenización (Tokenizer)

  * **Objetivo:** Dividir el texto crudo en unidades individuales llamadas **tokens** (generalmente palabras).
  * **Proceso:** Toma una cadena de texto larga y la convierte en una lista de palabras, eliminando espacios en blanco.
  * **En Spark:** Usamos `Tokenizer`.

<!-- end list -->

```python
from pyspark.ml.feature import Tokenizer

# inputCol: la columna con el texto original.
# outputCol: la nueva columna que contendrá la lista de tokens.
tokenizer = Tokenizer(inputCol="text", outputCol="tokens")
books = tokenizer.transform(books)

# Resultado: Una columna 'tokens' con listas de palabras [hola, mundo, ...]
```

#### 2\. Eliminación de Signos de Puntuación

  * **Objetivo:** Limpiar los tokens para que "hola." y "hola" sean tratados como la misma palabra.
  * **En Spark:** A menudo se usa expresiones regulares (`regexp_replace`) antes o después de tokenizar.

<!-- end list -->

```python
from pyspark.sql.functions import regexp_replace

# Regular expression (REGEX) to match commas and hyphens
REGEX = '[,\\-]'

# Eliminar comas, guiones y otros signos usando REGEX reemplazandolos por espacio
books = books.withColumn('text', regexp_replace(books.text, REGEX, ' '))
```

#### 3\. Eliminación de "Stop Words" (Palabras Vacías)

  * **Objetivo:** Eliminar palabras muy comunes que **no transmiten mucha información** semántica (ej. "el", "la", "y", "en", "a"). Esto reduce el ruido y el tamaño de los datos.
  * **En Spark:** Usamos `StopWordsRemover`. Spark tiene listas predefinidas de estas palabras para muchos idiomas.

<!-- end list -->

```python
from pyspark.ml.feature import StopWordsRemover

# Definir el eliminador de stop words
stopwords = StopWordsRemover()

# Ver la lista de palabras que eliminará (en inglés por defecto)
# print(stopwords.getStopWords())

# Aplicar la transformación: toma 'tokens' y crea 'words' sin las stop words
stopwords = stopwords.setInputCol('tokens').setOutputCol('words')
books = stopwords.transform(books)
```

#### 4\. Vectorización (Feature Hashing / TF-IDF)

  * **Objetivo:** Convertir la lista de palabras limpias en números.
  * **HashingTF (Term Frequency):** Cuenta la frecuencia de cada palabra en el documento y la mapea a un índice numérico usando una función hash. Es muy eficiente para grandes vocabularios.
  * **IDF (Inverse Document Frequency):** (Opcional pero recomendado) Ajusta el conteo para dar menos peso a palabras que aparecen en *muchos* documentos (aunque no sean "stop words") y más peso a las que son raras y específicas de un documento.

<!-- end list -->

```python
from pyspark.ml.feature import HashingTF, IDF

# 1. HashingTF: Convierte palabras a vectores de frecuencia cruda
# numFeatures: define el tamaño del vector resultante (ej. 32 para pruebas pequeñas, mucho mayor en producción)
hasher = HashingTF(inputCol="words", outputCol="raw_features", numFeatures=32)
books = hasher.transform(books)

# 2. IDF: Re-escala los vectores para dar más importancia a palabras raras
idf = IDF(inputCol="raw_features", outputCol="features")
idf_model = idf.fit(books)
books = idf_model.transform(books)
```

Al final de este proceso, tienes una columna `features` que es un vector numérico listo para ser usado por cualquier algoritmo de ML en Spark (como Regresión Logística o Árboles de Decisión).