# Import class for creating a pipeline
from pyspark.ml import Pipeline

# Construct a pipeline
# Las etapas ya están definidas: indexer, onehot, assembler, regression
pipeline = Pipeline(stages=[indexer, onehot, assembler, regression])

# Train the pipeline on the training data
# El método .fit() ejecuta todo el flujo en los datos de entrenamiento
pipeline_model = pipeline.fit(flights_train)

# Make predictions on the testing data
# El método .transform() aplica las mismas transformaciones y el modelo entrenado a los datos de prueba
predictions = pipeline_model.transform(flights_test)