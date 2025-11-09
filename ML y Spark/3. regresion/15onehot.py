# Import the one hot encoder class
from pyspark.ml.feature import OneHotEncoder

# Create an instance of the one hot encoder
# inputCols: lista de columnas con índices numéricos (salida de StringIndexer)
# outputCols: lista de nombres para las nuevas columnas de vectores dispersos
onehot = OneHotEncoder(inputCols=['org_idx'], outputCols=['org_dummy'])

# Apply the one hot encoder to the flights data
# Primero ajustamos (fit) el modelo a los datos para que conozca las categorías
onehot_model = onehot.fit(flights)
# Luego transformamos los datos
flights_onehot = onehot_model.transform(flights)

# Check the results
# Seleccionamos las columnas relevantes, tomamos valores únicos y ordenamos para verificar la asignación
flights_onehot.select('org', 'org_idx', 'org_dummy').distinct().sort('org_idx').show()