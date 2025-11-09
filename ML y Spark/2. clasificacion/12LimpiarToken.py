# Import the necessary functions
from pyspark.sql.functions import regexp_replace
from pyspark.ml.feature import Tokenizer

# Remove punctuation (REGEX provided) and numbers
# Se reemplazan los caracteres de puntuación [_():;,.!?\-] por un espacio ' '
wrangled = sms.withColumn('text', regexp_replace(sms.text, '[_():;,.!?\\-]', ' '))
# Se reemplazan los números [0-9] por un espacio ' '
wrangled = wrangled.withColumn('text', regexp_replace(wrangled.text, '[0-9]', ' '))

# Merge multiple spaces
# Se fusionan múltiples espacios consecutivos en uno solo
wrangled = wrangled.withColumn('text', regexp_replace(wrangled.text, ' +', ' '))

# Split the text into words
# Se utiliza Tokenizer para dividir el texto en palabras individuales (tokens)
wrangled = Tokenizer(inputCol='text', outputCol='words').transform(wrangled)

wrangled.show(4, truncate=False)