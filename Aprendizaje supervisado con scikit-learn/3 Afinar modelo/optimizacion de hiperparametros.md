La **optimización de hiperparámetros** (Hyperparameter Tuning) es el proceso de encontrar la configuración ideal para nuestro modelo antes de que este comience a aprender. Si los parámetros son lo que el modelo aprende de los datos (como los coeficientes de una regresión), los **hiperparámetros** son las "perillas" que nosotros ajustamos manualmente para guiar ese aprendizaje.

---

## Optimización de Hiperparámetros: GridSearchCV y RandomizedSearchCV

### 1. ¿Qué es el Hyperparameter Tuning?

Como ingenieros, no queremos adivinar si $k=3$ o $k=7$ es mejor para KNN, o si $\alpha=0.1$ es mejor que $\alpha=100$. Queremos un proceso sistemático que pruebe múltiples valores y elija el ganador basado en el rendimiento de **validación cruzada** sobre el conjunto de entrenamiento.

> ⚠️ **Regla de Oro:** Siempre reservamos el **test set** hasta el final. La optimización se hace sobre el **train set** usando validación cruzada para evitar que los hiperparámetros se "sobreajusten" a los datos de prueba.

---

### 2. Búsqueda en Cuadrícula (GridSearchCV)

Este método es exhaustivo. Definimos una "rejilla" de valores posibles y el modelo prueba **todas las combinaciones posibles**.

- **Ejemplo:** Si probamos 3 valores de `n_neighbors` y 2 tipos de métricas de distancia (`euclidean` y `manhattan`), GridSearchCV realizará 6 experimentos por cada pliegue (fold) de validación cruzada.
    

```python
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.linear_model import Ridge

# 1. Definir el espacio de búsqueda (Diccionario)
param_grid = {"alpha": [0.0001, 0.001, 0.01, 0.1, 1.0]}

# 2. Configurar validación cruzada y modelo
kf = KFold(n_splits=5, shuffle=True, random_state=42)
ridge = Ridge()

# 3. Instanciar GridSearchCV
ridge_cv = GridSearchCV(ridge, param_grid, cv=kf)

# 4. Ajustar a los datos de entrenamiento
ridge_cv.fit(X_train, y_train)

# 5. Obtener los mejores resultados
print("Mejores parámetros: {}".format(ridge_cv.best_params_))
print("Mejor puntuación (R^2): {}".format(ridge_cv.best_score_))
```

---

### 3. Búsqueda Aleatoria (RandomizedSearchCV)

GridSearchCV tiene un problema de **escalabilidad**. Si tienes muchos hiperparámetros y muchos valores, el número de entrenamientos explota (ej. 3 hiperparámetros $\times$ 10 valores $\times$ 10 folds = 1000 fits).

**RandomizedSearchCV** soluciona esto seleccionando combinaciones al azar.

- **Ventaja:** Es mucho más rápido y computacionalmente eficiente.
    
- **n_iter:** Este parámetro controla cuántas combinaciones aleatorias se probarán.
    

```python
from sklearn.model_selection import RandomizedSearchCV

# Se usa igual que GridSearchCV pero con n_iter
ridge_rv = RandomizedSearchCV(ridge, param_grid, cv=kf, n_iter=2)
ridge_rv.fit(X_train, y_train)

print("Mejores parámetros (Random): {}".format(ridge_rv.best_params_))
```

---

### 4. Resumen Comparativo

|**Característica**|**GridSearchCV**|**RandomizedSearchCV**|
|---|---|---|
|**Exhaustividad**|Prueba TODAS las combinaciones.|Prueba una selección aleatoria.|
|**Costo Computacional**|Muy alto (Lento).|Bajo (Rápido).|
|**Uso Ideal**|Pocos parámetros y valores.|Muchos parámetros o datasets grandes.|
|**Riesgo**|Puede tardar horas o días.|Puede saltarse la combinación óptima.|

### Evaluación Final

Una vez que el objeto de búsqueda (sea Grid o Random) termina de ajustarse, podemos usarlo directamente para evaluar el **test set**:

```python
# Evaluamos el modelo tuneado con datos nunca vistos
test_score = ridge_cv.score(X_test, y_test)
print("Precisión en el Test Set: {}".format(test_score))
```

---

### Concepto de Ingeniería (DevOps/SysAdmin)

En un flujo de **CI/CD para Machine Learning**, GridSearchCV suele ser demasiado pesado para pipelines frecuentes. RandomizedSearchCV es el estándar preferido cuando se busca un equilibrio entre rendimiento y tiempo de ejecución en servidores de entrenamiento.
