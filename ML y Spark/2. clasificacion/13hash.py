from pyspark.ml.feature import StopWordsRemover, HashingTF, IDF

# Remove stopwords
# Se crea un StopWordsRemover que toma la columna 'words' y genera 'terms'
wrangled = StopWordsRemover(inputCol='words', outputCol='terms')\
      .transform(sms)

# Apply the hashing trick
# Se aplica HashingTF a la columna 'terms' para crear vectores de frecuencia cruda 'hash'
# numFeatures=1024 define el tamaño del vector hash
wrangled = HashingTF(inputCol='terms', outputCol='hash', numFeatures=1024)\
      .transform(wrangled)

# Convert hashed symbols to TF-IDF
# Se ajusta y transforma usando IDF para re-escalar los vectores 'hash' a 'features'
tf_idf = IDF(inputCol='hash', outputCol='features')\
      .fit(wrangled).transform(wrangled)

tf_idf.select('terms', 'features').show(4, truncate=False)