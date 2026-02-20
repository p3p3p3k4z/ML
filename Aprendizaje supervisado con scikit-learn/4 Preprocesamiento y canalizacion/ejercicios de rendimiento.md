Para cerrar este ciclo de aprendizaje supervisado, realizaremos una comparativa entre tres de los algoritmos de clasificación más utilizados. En este caso, el objetivo es predecir si una canción será popular o no (un problema binario basado en la mediana). Esta técnica de "torneo de modelos" nos permite ver cuál se adapta mejor a la estructura de los datos de música después de haber sido escalados.


```python
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, cross_val_score

# 1. Crear el diccionario de modelos
models = {
    "Logistic Regression": LogisticRegression(), 
    "KNN": KNeighborsClassifier(), 
    "Decision Tree Classifier": DecisionTreeClassifier()
}
results = []

# 2. Recorrer los valores del diccionario
for model in models.values():
  
  # 3. Instanciar el objeto KFold (6 divisiones, semilla 12)
  kf = KFold(n_splits=6, random_state=12, shuffle=True)
  
  # 4. Realizar la validación cruzada
  # Se usan los datos escalados para una comparativa justa
  cv_results = cross_val_score(model, X_train_scaled, y_train, cv=kf)
  results.append(cv_results)

# 5. Visualización de resultados
plt.boxplot(results, labels=models.keys())
plt.ylabel("Accuracy")
plt.title("Comparativa de Clasificadores: Popularidad Musical")
plt.show()
```

---

### Análisis de la Comparativa de Clasificación

En este ejercicio introducimos un nuevo contendiente: el **Árbol de Decisión**, y lo ponemos a prueba junto a los modelos que ya dominas.

#### ¿Por qué usar un Boxplot para clasificar?

El diagrama de cajas no solo nos dice cuál modelo tiene la **Accuracy** (exactitud) más alta en promedio, sino que nos revela la **varianza** del modelo:

- **Logistic Regression:** Suele ser muy estable y funciona bien si las clases son linealmente separables.
    
- **KNN:** Su rendimiento depende drásticamente de que el escalado sea perfecto, ya que se basa en distancias.
    
- **Decision Tree:** Es un modelo muy flexible que no asume linealidad. Sin embargo, tiende al sobreajuste si no se limita su profundidad.
    

#### El papel del KFold (n_splits=6)

Al dividir los datos en 6 partes, estamos entrenando cada modelo 6 veces con diferentes subconjuntos. Esto es vital para asegurar que el modelo ganador no lo sea por "suerte" de haber recibido datos fáciles, sino por su capacidad real de generalización.

#### Interpretación de Resultados

Si al ejecutar el código ves que el **Decision Tree** tiene una caja muy grande o dispersa, significa que es inestable ante cambios en los datos. Si la **Regresión Logística** tiene la línea naranja (mediana) más alta y una caja compacta, sería tu elección ideal para llevar a producción en este problema de popularidad.

---
