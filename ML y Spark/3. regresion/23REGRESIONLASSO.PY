from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

# Fit Lasso model (λ = 1, α = 1) to training data
# elasticNetParam=1 indica Lasso (penalización L1)
# regParam=1 es la fuerza de la penalización (λ)
regression = LinearRegression(labelCol='duration', regParam=1, elasticNetParam=1).fit(flights_train)

# Calculate the RMSE on testing data
rmse = RegressionEvaluator(labelCol='duration', metricName='rmse').evaluate(regression.transform(flights_test))
print("The test RMSE is", rmse)

# Look at the model coefficients
coeffs = regression.coefficients
print(coeffs)

# Number of zero coefficients
# Contamos cuántos coeficientes fueron reducidos exactamente a 0.0 por Lasso
zero_coeff = sum([beta == 0.0 for beta in regression.coefficients])
print("Number of coefficients equal to 0:", zero_coeff)