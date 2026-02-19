Este es uno de los temas más cruciales en Machine Learning. No basta con que el modelo haga predicciones; necesitamos saber si son **buenas** y si el modelo realmente aprendió o simplemente "memorizó" las respuestas.

---

## Medir el rendimiento del modelo

En clasificación, la métrica más utilizada es la **Exactitud (Accuracy)**.

- **Definición:** Es el número de predicciones correctas dividido por el número total de observaciones.
    
- **El Problema:** Si evaluamos el modelo con los mismos datos que usamos para entrenarlo, los resultados serán engañosamente altos. El modelo ya conoce las respuestas, por lo que no estaríamos midiendo su capacidad para **generalizar** a datos nuevos.
    

> 💡 **Analogía del examen:** Si un profesor te da las preguntas y respuestas de un examen el día anterior, y sacas 10, no significa que sepas la materia; significa que tienes buena memoria. Para saber si aprendiste, el profesor debe ponerte **preguntas que nunca has visto**.

---

### División de Entrenamiento y Prueba (Train/Test Split)

Para medir la capacidad real del modelo, dividimos nuestros datos en dos grupos:

1. **Conjunto de Entrenamiento (Training set):** Se usa para ajustar (entrenar) el clasificador.
    
2. **Conjunto de Prueba (Test set):** Se usa para calcular la exactitud del modelo sobre etiquetas que no conoce.
    

#### Parámetros clave en `train_test_split`

Al realizar esta división con scikit-learn, usamos tres argumentos fundamentales:

- **`test_size`:** Define qué porcentaje de los datos se irá a la prueba. Lo común es entre **0.2 (20%) y 0.3 (30%)**.
    
- **`random_state`:** Es una "semilla" para el generador de números aleatorios. Usar el mismo número (ej. 42) asegura que el split sea el mismo cada vez que corras el código, permitiendo **reproducibilidad**.
    
- **`stratify=y`:** Asegura que la proporción de las etiquetas en los conjuntos de entrenamiento y prueba sea igual a la de los datos originales.
    
    - _Ejemplo:_ Si el 10% de tus clientes abandonan la empresa (_churn_), el `stratify` garantiza que tanto en tu entrenamiento como en tu prueba haya un 10% de casos de abandono.
        


```python
from sklearn.model_selection import train_test_split

# Dividimos en 4 arreglos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, 
                                                    random_state=21, 
                                                    stratify=y)

# Entrenamos solo con el conjunto de entrenamiento
knn.fit(X_train, y_train)

# Evaluamos con el conjunto de prueba
print(knn.score(X_test, y_test))
```

---

### Complejidad del Modelo: El papel de "k"

El valor de $k$ (número de vecinos) determina qué tan complejo es nuestro modelo.

- **$k$ Pequeño (ej. $k=1$):** El modelo es muy **complejo**. Se fija en cada detalle individual y es muy sensible al "ruido" de los datos. Esto causa **Sobreajuste (Overfitting)**: le va excelente en el entrenamiento pero mal en la prueba.
    
- **$k$ Grande (ej. $k=100$):** El modelo es muy **simple**. La frontera de decisión se vuelve muy suave y no logra detectar patrones importantes. Esto causa **Ajuste Insuficiente (Underfitting)**: le va mal tanto en entrenamiento como en prueba.
    

![overfitting and underfitting in machine learning, generada por IA](https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSm4luNmuoM-FmxEKTfZjqxZVG1NdmRefLK18SJKMaz9zCoJJswSV1qx8wA8ewBfIC3SYbZJ9hoI6fRAOS6maYg7UORjzEpFyMbrv_JfjxdJSEI0jI)

---

### Curva de Complejidad del Modelo

Para encontrar el "punto dulce" de $k$, los científicos de datos grafican la exactitud del entrenamiento y de la prueba contra diferentes valores de $k$.

1. Se crean varios modelos variando $k$ (usando un bucle `for`).
    
2. Se guardan las precisiones de entrenamiento y prueba.
    
3. Se grafican los resultados.
    

**Interpretación de la curva:**

- A la **izquierda** (valores de $k$ bajos), verás mucha separación entre la curva de entrenamiento (muy alta) y la de prueba (baja). Eso es **Overfitting**.
    
- A la **derecha** (valores de $k$ altos), ambas curvas empiezan a bajar y a parecerse. Eso es **Underfitting**.
    
- **El k ideal:** Es el punto donde la exactitud de la **prueba** alcanza su máximo valor antes de empezar a descender. Según tus notas, en ese conjunto de datos específico, el pico ocurre cerca de **$k=13$**.
    
