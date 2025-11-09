# Split into training and testing sets in a 80:20 ratio
# seed=43 para garantizar la repetibilidad como se pide.
flights_train, flights_test = flights.randomSplit([0.8, 0.2], seed=43)

# Check that training set has around 80% of records
# Dividimos el conteo del conjunto de entrenamiento por el conteo total del dataset original.
training_ratio = flights_train.count() / flights.count()
print(training_ratio)