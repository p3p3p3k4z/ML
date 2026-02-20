Este ejercicio es fundamental para visualizar el concepto del "punto dulce" en el Machine Learning. Al probar diferentes valores de $k$, estamos buscando el equilibrio perfecto entre un modelo que memoriza (sobreajuste) y uno que no aprende lo suficiente (infraajuste).

---

## Análisis de Sobreajuste e Infraajuste

El objetivo de evaluar la complejidad del modelo es encontrar un punto donde el algoritmo generalice bien ante nuevas observaciones, evitando los dos errores clásicos:

- **Sobreajuste (Overfitting):** El modelo es demasiado complejo y se ajusta perfectamente a los datos de entrenamiento pero falla con los de prueba.
    
- **Infraajuste (Underfitting):** El modelo es demasiado simple y no logra capturar la relación entre las características y el objetivo.
    

### Implementación del ciclo de evaluación

Para encontrar el valor óptimo de $k$, iteramos sobre un rango de vecinos y almacenamos su precisión.

```python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# 1. Crear el rango de vecinos (1 a 12 inclusive)
neighbors = np.arange(1, 13)
train_accuracies = {}
test_accuracies = {}

for neighbor in neighbors:
  
	# 2. Instanciar el modelo con el iterador actual
	knn = KNeighborsClassifier(n_neighbors=neighbor)
  
	# 3. Ajustar el modelo a los datos de entrenamiento
	knn.fit(X_train, y_train)
  
	# 4. Calcular y almacenar precisiones
	# Usamos .score() que devuelve la exactitud (accuracy)
	train_accuracies[neighbor] = knn.score(X_train, y_train)
	test_accuracies[neighbor] = knn.score(X_test, y_test)
print(neighbors, '\n', train_accuracies, '\n', test_accuracies)
```

---

### Visualización: La Curva de Complejidad

Una vez que tenemos los datos, el siguiente paso es graficarlos para tomar una decisión informada. El código de complemento utiliza `matplotlib` para generar esta curva.

```python
import matplotlib.pyplot as plt

# Configurar el gráfico
plt.figure(figsize=(8, 6))
plt.title('KNN: Variando el número de vecinos')

# Graficar precisión de entrenamiento
plt.plot(neighbors, train_accuracies.values(), label='Precisión Entrenamiento')

# Graficar precisión de prueba
plt.plot(neighbors, test_accuracies.values(), label='Precisión Prueba')

plt.legend()
plt.xlabel('Número de Vecinos (k)')
plt.ylabel('Exactitud (Accuracy)')
plt.show()
```

### Interpretación de la gráfica

Al observar la curva resultante, podemos identificar el comportamiento del modelo:

- **A la izquierda ($k$ bajos):** Notarás que la precisión del entrenamiento es muy alta (cercana al 1.0), mientras que la de prueba es menor. Aquí el modelo está **sobreajustado**.
    
- **A la derecha ($k$ altos):** Ambas precisiones tienden a bajar y estabilizarse. Si bajan demasiado, el modelo está **infraajustado**.
    
- **El punto óptimo:** Es el valor de $k$ en el eje horizontal donde la **Precisión de Prueba** alcanza su valor máximo. Este es el modelo que mejor generalizará con datos reales del mundo de las telecomunicaciones.
    
Este es el paso final para cerrar el ciclo de evaluación de tu modelo. Generar la gráfica te permite ver de forma clara qué valor de $k$ es el más equilibrado.

Aquí tienes el código completado y la explicación de cómo interpretar lo que verás en pantalla.

---

## Visualizar la complejidad del modelo

Una vez que hemos probado distintos valores para el número de vecinos ($k$), la mejor forma de tomar una decisión es mediante una **Curva de Complejidad**. Esta gráfica nos muestra cómo cambia la exactitud (accuracy) tanto en los datos que el modelo ya conoce (entrenamiento) como en los que son nuevos para él (prueba).


```python
import matplotlib.pyplot as plt

# 1. Añadimos el título al gráfico
plt.title("KNN: Varying Number of Neighbors")

# 2. Trazamos la precisión de entrenamiento
# Usamos .values() porque las precisiones están guardadas en un diccionario
plt.plot(neighbors, train_accuracies.values(), label="Training Accuracy")

# 3. Trazamos la precisión de prueba
plt.plot(neighbors, test_accuracies.values(), label="Testing Accuracy")

# Configuraciones adicionales para que el gráfico sea legible
plt.legend()
plt.xlabel("Number of Neighbors")
plt.ylabel("Accuracy")

# 4. Visualizamos el gráfico final
plt.show()
```

---

### ¿Cómo interpretar este apunte visual?

Para entender esta gráfica, imagina que estás calibrando la sensibilidad de un sensor:

- **La línea de "Training Accuracy" (Entrenamiento):** Siempre suele empezar muy alta cuando $k$ es pequeño. Esto es porque con pocos vecinos, el modelo es muy "detallista" y se acuerda perfectamente de casi todos los puntos de entrenamiento. A medida que $k$ aumenta, esta línea suele bajar porque el modelo se vuelve más general.
    
- **La línea de "Testing Accuracy" (Prueba):** Esta es la que realmente nos importa.
    
    - Si $k$ es muy bajo, la precisión de prueba es baja comparada con la de entrenamiento (**Sobreajuste**).
        
    - Si $k$ es muy alto, ambas líneas bajan porque el modelo se vuelve "perezoso" y no distingue patrones (**Infraajuste**).
        

> 💡 **El punto ideal:** Debes buscar el punto más alto en la línea de **Testing Accuracy**. En el conjunto de datos de _churn_ que estás usando, verás que el mejor rendimiento se encuentra cuando el número de vecinos es aproximadamente **7 o 9**. Ese es el valor de $k$ que deberías elegir para tu modelo final.

