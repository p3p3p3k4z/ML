from pyspark.ml.evaluation import RegressionEvaluator

# Find the RMSE on testing data
rmse = RegressionEvaluator(labelCol='duration', metricName='rmse').evaluate(predictions)
print("The test RMSE is", rmse)

# Average minutes on ground at OGG for flights departing between 21:00 and 24:00
# OGG es el aeropuerto de referencia y 21:00-24:00 es el horario de referencia.
avg_eve_ogg = regression.intercept
print(avg_eve_ogg)

# Average minutes on ground at OGG for flights departing between 03:00 and 06:00
# 03:00-06:00 corresponde al bucket 1, que está en el índice 9 de los coeficientes.
avg_night_ogg = regression.intercept + regression.coefficients[9]
print(avg_night_ogg)

# Average minutes on ground at JFK for flights departing between 03:00 and 06:00
# JFK está en el índice 3. 03:00-06:00 está en el índice 9.
avg_night_jfk = regression.intercept + regression.coefficients[3] + regression.coefficients[9]
print(avg_night_jfk)