from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

# Create a regression object and train on training data
# Especificamos la columna objetivo (labelCol) como 'duration' y la columna de características como 'km'.
# Es importante notar que LinearRegression espera una columna de características vectorizada por defecto ('features'),
# pero si solo usamos una columna numérica simple como 'km', Spark a veces puede manejarlo directamente o requerir VectorAssembler antes.
# Asumiendo que 'km' ya fue vectorizada o que el entorno lo maneja, la instrucción básica es:
regression = LinearRegression(labelCol='duration').fit(flights_train)

# NOTA: Si 'km' no es un vector, necesitarías un paso previo con VectorAssembler:
# assembler = VectorAssembler(inputCols=['km'], outputCol='features')
# flights_train = assembler.transform(flights_train)
# flights_test = assembler.transform(flights_test)
# regression = LinearRegression(labelCol='duration', featuresCol='features').fit(flights_train)

# Create predictions for the testing data and take a look at the predictions
predictions = regression.transform(flights_test)
predictions.select('duration', 'prediction').show(5, False)

# Calculate the RMSE
# Usamos RegressionEvaluator especificando la métrica 'rmse' y la columna objetivo real 'duration'.
RegressionEvaluator(labelCol='duration', metricName='rmse').evaluate(predictions)