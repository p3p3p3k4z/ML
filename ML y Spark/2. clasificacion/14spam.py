# Split the data into training and testing sets
# División 4:1 significa 80% entrenamiento, 20% prueba.
sms_train, sms_test = sms.randomSplit([0.8, 0.2], seed=13)

# Fit a Logistic Regression model to the training data
# Se usa regParam=0.2 como se solicitó en las instrucciones.
logistic = LogisticRegression(regParam=0.2).fit(sms_train)

# Make predictions on the testing data
prediction = logistic.transform(sms_test)

# Create a confusion matrix, comparing predictions to known labels
prediction.groupBy('label', 'prediction').count().show()