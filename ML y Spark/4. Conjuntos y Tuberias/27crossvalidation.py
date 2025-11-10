from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

# Create an empty parameter grid
# Incluso si está vacía, CrossValidator la necesita para saber qué combinaciones probar (aquí solo 1).
params = ParamGridBuilder().build()

# Create objects for building and evaluating a regression model
# El modelo debe predecir la columna 'duration'.
regression = LinearRegression(labelCol='duration')
# Usaremos RMSE como métrica de evaluación.
evaluator = RegressionEvaluator(labelCol='duration', metricName='rmse')

# Create a cross validator
# numFolds=5 para validación cruzada de 5 pliegues.
cv = CrossValidator(estimator=regression,
                    estimatorParamMaps=params,
                    evaluator=evaluator,
                    numFolds=5)

# Train and test model on multiple folds of the training data
# .fit() ejecuta el proceso de 5-fold CV.
cv = cv.fit(flights_train)

# NOTE: Since cross-validation builds multiple models, the fit() method can take a little while to complete.