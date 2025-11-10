from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Create a random forest classifier
# Se crea el estimador base.
forest = RandomForestClassifier()

# Create a parameter grid
# Se añaden las cuadrículas para 'featureSubsetStrategy' y 'maxDepth' como se solicitó.
params = ParamGridBuilder() \
            .addGrid(forest.featureSubsetStrategy, ['all', 'onethird', 'sqrt', 'log2']) \
            .addGrid(forest.maxDepth, [2, 5, 10]) \
            .build()

# Create a binary classification evaluator
# Usamos este evaluador porque estamos prediciendo si un vuelo se retrasa (1) o no (0).
# Por defecto usa la métrica 'areaUnderROC'.
evaluator = BinaryClassificationEvaluator()

# Create a cross-validator
# Configuramos el validador cruzado con el estimador (forest), la cuadrícula (params),
# el evaluador y el número de pliegues (5).
cv = CrossValidator(estimator=forest,
                    estimatorParamMaps=params,
                    evaluator=evaluator,
                    numFolds=5)