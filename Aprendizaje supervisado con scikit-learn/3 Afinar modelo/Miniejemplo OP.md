El proceso de optimización mediante **GridSearchCV** permite automatizar la búsqueda del mejor hiperparámetro para un modelo. En este caso, buscaremos el valor óptimo de **Alpha** para una regresión **Lasso**, evaluando cómo diferentes niveles de penalización afectan la precisión al predecir los niveles de glucosa en sangre. Utilizaremos el conjunto de datos `diabetes_df` y validación cruzada para asegurar que el parámetro elegido sea robusto y no dependa de una sola partición de los datos.


```python
# Importar GridSearchCV
from sklearn.model_selection import GridSearchCV

# 1. Configurar la cuadrícula de parámetros para "alpha"
# Usamos np.linspace para generar 20 valores entre 0.00001 y 1
param_grid = {"alpha": np.linspace(0.00001, 1, 20)}

# 2. Instanciar lasso_cv
lasso_cv = GridSearchCV(lasso, param_grid, cv=kf)

# 3. Ajustar a los datos de entrenamiento
lasso_cv.fit(X_train, y_train)

# 4. Realizar las impresiones con el formato exacto requerido
print("Tuned lasso paramaters: {}".format(lasso_cv.best_params_))
print("Tuned lasso score: {}".format(lasso_cv.best_score_))
```

---

### Análisis de la Optimización con GridSearchCV

Esta técnica transforma la selección de hiperparámetros de un proceso de "prueba y error" manual a un flujo de trabajo científico y reproducible:

- **`np.linspace(0.00001, 1, 20)`**: Esta función es extremadamente útil para generar el espacio de búsqueda. En lugar de escribir manualmente una lista de números, definimos un rango y le pedimos a NumPy que cree una cantidad específica de valores (en este caso, 20) con la misma distancia entre ellos.
    
- **Funcionamiento de `GridSearchCV`**: Al llamar a `.fit()`, el objeto realiza el producto cartesiano de todos los parámetros en la rejilla. Por cada valor de Alpha, entrena el modelo `kf` veces (según el número de pliegues definidos en `KFold`). Si `kf` tiene 5 pliegues y tenemos 20 valores de Alpha, el sistema realiza **100 ajustes** en total.
    
- **Atributos de resultados**:
    
    - **`.best_params_`**: Devuelve un diccionario con la combinación de parámetros que obtuvo el mejor rendimiento promedio en la validación cruzada.
        
    - **`.best_score_`**: Devuelve la media de la métrica (R-cuadrado para regresión) obtenida por el mejor modelo. Es importante recordar que este puntaje se calcula sobre los pliegues de validación del conjunto de entrenamiento.
        
- **Ventaja competitiva**: Utilizar `GridSearchCV` garantiza que hemos explorado el espacio de configuración de manera exhaustiva dentro de los límites definidos, lo que suele resultar en modelos con una capacidad de generalización significativamente superior.

---
Cuando el espacio de búsqueda de hiperparámetros es muy amplio, utilizar `GridSearchCV` puede resultar extremadamente costoso en términos de tiempo y recursos. Para solucionar esto, utilizamos `RandomizedSearchCV`, que en lugar de probar todas las combinaciones posibles, selecciona un número fijo de configuraciones de forma aleatoria a partir de las distribuciones que definamos. En este ejercicio, optimizaremos un modelo de regresión logística para predecir la diabetes, ajustando la penalización, la tolerancia, la fuerza de regularización ($C$) y el peso de las clases para manejar posibles desequilibrios en los datos.

Python

```
import numpy as np
from sklearn.model_selection import RandomizedSearchCV

# 1. Crear el espacio de parámetros
# Definimos las opciones para penalización, tolerancia, C y pesos de clase
params = {"penalty": ["l1", "l2"],
         "tol": np.linspace(0.0001, 1.0, 50),
         "C": np.linspace(0.1, 1.0, 50),
         "class_weight": ["balanced", {0: 0.8, 1: 0.2}]}

# 2. Instanciar el objeto RandomizedSearchCV
# Pasamos el modelo logreg, el diccionario params y el esquema de validación kf
logreg_cv = RandomizedSearchCV(logreg, params, cv=kf)

# 3. Ajustar el modelo a los datos de entrenamiento
# El proceso realizará búsquedas aleatorias y validación cruzada simultáneamente
logreg_cv.fit(X_train, y_train)

# 4. Imprimir los parámetros optimizados y la mejor puntuación de precisión
print("Tuned Logistic Regression Parameters: {}".format(logreg_cv.best_params_))
print("Tuned Logistic Regression Best Accuracy Score: {}".format(logreg_cv.best_score_))
```

---

### Análisis de RandomizedSearchCV y sus Hiperparámetros

Esta técnica es el estándar en la industria cuando se trabaja con modelos complejos o grandes volúmenes de datos, ya que permite obtener resultados muy cercanos a la búsqueda exhaustiva en una fracción del tiempo.

#### 1. ¿Por qué usar RandomizedSearchCV?

A diferencia de la búsqueda en cuadrícula, donde el número de "fits" es el producto de todas las opciones, aquí el costo está controlado. Si tienes 4 hiperparámetros con 50 valores cada uno, `GridSearchCV` haría miles de entrenamientos. `RandomizedSearchCV` por defecto realiza solo 10 iteraciones (aunque se puede ajustar con `n_iter`), eligiendo puntos al azar en el espacio de búsqueda.

#### 2. Desglose de los Parámetros de Regresión Logística

- **`penalty`**: Selecciona entre **l1 (Lasso)** y **l2 (Ridge)**. Como vimos anteriormente, l1 puede eliminar características irrelevantes, mientras que l2 reduce su impacto.
    
- **`C`**: Controla la fuerza de la regularización. Un valor pequeño de $C$ especifica una regularización más fuerte (penaliza más los coeficientes grandes).
    
- **`tol` (Tolerancia)**: Define el criterio de parada para los algoritmos de optimización. Indica qué tan precisa debe ser la búsqueda de la solución antes de detenerse.
    
- **`class_weight`**: Es una herramienta vital para el **desequilibrio de clases**.
    
    - `"balanced"` ajusta automáticamente los pesos de forma inversamente proporcional a las frecuencias de las clases.
        
    - El diccionario `{0: 0.8, 1: 0.2}` permite asignar pesos manuales si sabemos que una clase es más importante o frecuente que otra.
        

#### 3. Evaluación del modelo "Tuneado"

Al finalizar el proceso, los atributos `best_params_` y `best_score_` nos entregan la configuración ganadora. Este modelo optimizado está mucho mejor preparado para generalizar en el mundo real que un modelo con los parámetros por defecto, especialmente en un problema tan sensible como la predicción de salud.

¿Te gustaría que ahora pasáramos al apunte final sobre cómo manejar **datos categóricos** y valores faltantes para completar todo el flujo de preprocesamiento de datos?