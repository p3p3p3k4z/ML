from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF

# 1. Break text into tokens at non-word characters
tokenizer = Tokenizer(inputCol='text', outputCol='words')

# 2. Remove stop words
# Usamos tokenizer.getOutputCol() para obtener automáticamente 'words' como entrada
remover = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol='terms')

# 3. Apply the hashing trick and transform to TF-IDF
# Usamos remover.getOutputCol() -> 'terms'
hasher = HashingTF(inputCol=remover.getOutputCol(), outputCol="hash")
# Usamos hasher.getOutputCol() -> 'hash'
idf = IDF(inputCol=hasher.getOutputCol(), outputCol="features")

# 4. Create a logistic regression object and add everything to a pipeline
logistic = LogisticRegression()
pipeline = Pipeline(stages=[tokenizer, remover, hasher, idf, logistic])