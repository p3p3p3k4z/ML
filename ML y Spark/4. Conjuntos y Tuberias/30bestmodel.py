# Get the best model from cross validation
best_model = cv_model.bestModel

# Look at the stages in the best model
print(best_model.stages)

# Get the parameters for the LinearRegression object in the best model
# La regresión lineal es la cuarta etapa (índice 3)
best_model.stages[3].extractParamMap()

# Generate predictions on testing data using the best model then calculate RMSE
predictions = best_model.transform(flights_test)
print("RMSE =", evaluator.evaluate(predictions))