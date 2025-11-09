from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

# Create a regression object and train on training data
# Aquí usamos 'duration' como etiqueta (lo que queremos predecir)
# y 'features' como la columna de entrada (que ya debe contener 'km' y 'org_dummy' ensamblados).
regression = LinearRegression(labelCol='duration').fit(flights_train)

# Create predictions for the testing data
predictions = regression.transform(flights_test)

# Calculate the RMSE on testing data
# Evaluamos la raíz del error cuadrático medio (RMSE) comparando la predicción con la duración real.
RegressionEvaluator(labelCol='duration', metricName='rmse').evaluate(predictions)