# Average AUC for each parameter combination in grid
print(cv.avgMetrics)

# Average AUC for the best model
# max() porque AUC es mejor cuanto más alto sea.
print(max(cv.avgMetrics))

# What's the optimal parameter value for maxDepth?
# Accedemos al mejor modelo y explicamos el parámetro 'maxDepth'
print(cv.bestModel.explainParam('maxDepth'))
# What's the optimal parameter value for featureSubsetStrategy?
# Accedemos al mejor modelo y explicamos el parámetro 'featureSubsetStrategy'
print(cv.bestModel.explainParam('featureSubsetStrategy'))

# AUC for best model on testing data
# Usamos el mejor modelo (cv.bestModel) para transformar los datos de prueba y evaluamos.
print(evaluator.evaluate(cv.bestModel.transform(flights_test)))