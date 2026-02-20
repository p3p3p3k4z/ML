En este ejercicio final de regresión, compararemos tres algoritmos fundamentales: **Regresión Lineal**, **Ridge** y **Lasso**. El objetivo es predecir los niveles de "energy" en las canciones del dataset `music_df`. Al utilizar un bucle para evaluar múltiples modelos simultáneamente, podemos identificar no solo cuál es más preciso en promedio, sino cuál es más consistente a través de diferentes subconjuntos de datos gracias al diagrama de cajas.

```python
import matplotlib.pyplot as plt

# Diccionario de modelos para comparar
models = {"Linear Regression": LinearRegression(), 
          "Ridge": Ridge(alpha=0.1), 
          "Lasso": Lasso(alpha=0.1)}
results = []

# 1. Bucle para iterar sobre los modelos
for model in models.values():
  # Configurar la validación cruzada con el random_state correcto (42)
  kf = KFold(n_splits=6, random_state=42, shuffle=True)
  
  # 2. Realizar la validación cruzada
  cv_results = cross_val_score(model, X_train, y_train, cv=kf)
  
  # 3. Añadir los resultados a la lista
  results.append(cv_results)

# 4. Crear el diagrama de cajas (boxplot)
plt.boxplot(results, labels=models.keys())
plt.ylabel("R-squared")
plt.show()
```

---

### Análisis de la Comparativa de Regresión

Esta técnica es la forma más profesional de tomar una decisión basada en datos sobre qué algoritmo desplegar en producción.

#### 1. ¿Por qué estos tres modelos?

- **Linear Regression:** Es nuestra línea base. No tiene regularización y es el más simple.
    
- **Ridge:** Añade una penalización $L_2$ (al cuadrado de los coeficientes) para evitar que el modelo se vuelva demasiado complejo.
    
- **Lasso:** Añade una penalización $L_1$ (valor absoluto), lo que puede reducir algunos coeficientes a cero, realizando una selección automática de características.
    

#### 2. Interpretación del Boxplot

Al visualizar los resultados, no solo mires la línea central (la mediana). Fíjate en el tamaño de la caja:

- **Caja compacta:** Indica que el modelo es **robusto**. Independientemente de cómo dividas los datos, el error es similar.
    
- **Caja alargada o con valores atípicos (outliers):** Indica que el modelo es sensible a los datos de entrenamiento y podría sufrir de varianza alta.
    

#### 3. El R-cuadrado ($R^2$) como métrica

Recuerda que en este ejercicio estamos usando el coeficiente de determinación. Un valor más cercano a **1.0** indica que el modelo explica mejor la variabilidad de la "energía" de la canción. Si ves que Lasso tiene una puntuación mucho menor, es posible que el valor de `alpha=0.1` sea demasiado alto y esté eliminando características que sí eran importantes.

---

### Nota de Ingeniería (Enfoque DevOps)

Como aspirante a **SysAdmin/DevOps**, este patrón de código es altamente automatizable. Puedes integrar este script en un contenedor de Docker para que, cada vez que el equipo de ciencia de datos actualice el dataset, el sistema genere automáticamente este gráfico y lo envíe a un dashboard (como Grafana o un reporte de MLflow). Esto permite detectar de inmediato si un nuevo conjunto de datos ha hecho que el modelo previamente elegido deje de ser el óptimo.

---
Este es el momento de la verdad. Después de comparar modelos mediante validación cruzada, el paso final es enfrentarlos a los datos de prueba (**test set**). Esta es la evaluación definitiva porque utiliza datos que los modelos jamás han visto durante su entrenamiento. Usaremos el **RMSE** (_Root Mean Squared Error_), que nos da una medida del error en las mismas unidades que nuestro objetivo ("energy"), facilitando mucho la interpretación técnica.

```python
# Importar root_mean_squared_error de sklearn.metrics
from sklearn.metrics import root_mean_squared_error

# Iterar sobre el diccionario de modelos
for name, model in models.items():
  # Ajustar el modelo a los datos de entrenamiento escalados
  model.fit(X_train_scaled, y_train)
  
  # Hacer predicciones sobre el conjunto de pruebas escalado
  y_pred = model.predict(X_test_scaled)
  
  # Calcular el RMSE del conjunto de pruebas
  # Pasamos las etiquetas reales y las predicciones
  test_rmse = root_mean_squared_error(y_test, y_pred)
  print("{} Test Set RMSE: {}".format(name, test_rmse))
```

---

## Análisis Final: El Duelo de Regresores

En este ejercicio, estamos comparando la **Regresión Lineal** frente a **Ridge**. Como ingeniero, aquí tienes los puntos clave para interpretar estos resultados:

### ¿Qué nos dice el RMSE?

El RMSE cuantifica qué tan lejos, en promedio, están las predicciones del modelo de los valores reales. Al ser una raíz cuadrada, penaliza más fuertemente los errores grandes que el MAE (_Mean Absolute Error_).

- **Si el RMSE es bajo:** El modelo es preciso.
    
- **Si el RMSE de prueba es mucho mayor que el de entrenamiento:** Tienes un problema de **sobreajuste (overfitting)**.
    

### Regresión Lineal vs. Ridge

- **Linear Regression:** Intenta ajustar la línea que minimiza la suma de los errores al cuadrado sin restricciones. Si los datos tienen ruido, puede volverse demasiado compleja.
    
- **Ridge:** Introduce una penalización para mantener los coeficientes bajo control. Si el RMSE de Ridge es menor que el de la Regresión Lineal, significa que la regularización ayudó a que el modelo generalizara mejor.
    

---

> 💡 **Tip de Despliegue (DevOps/SysAdmin):** > En un flujo de trabajo profesional, el modelo que obtenga el RMSE más bajo en el **test set** es el que "empaquetarías" (usando librerías como `joblib` o `pickle`) para subirlo a un servidor de producción. Recuerda siempre guardar también el objeto `scaler`, ya que las predicciones en vivo necesitarán ser escaladas exactamente con los mismos parámetros de media y varianza que usaste aquí.
