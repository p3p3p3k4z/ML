La validación cruzada es una herramienta esencial para maximizar el uso de los datos disponibles, permitiendo que cada observación sea utilizada tanto para el entrenamiento como para la prueba. En este ejercicio, implementaremos una validación cruzada de 6 pliegues utilizando el gasto en **redes sociales** para predecir las **ventas**. El objetivo es observar la consistencia del modelo analizando el puntaje individual de cada uno de los pliegues (_folds_).

```python
# Importar los módulos necesarios
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression

# Crear el objeto KFold
# Configuramos 6 divisiones, barajamos los datos y fijamos la semilla en 5
kf = KFold(n_splits=6, shuffle=True, random_state=5)

# Instanciar el modelo de regresión lineal
reg = LinearRegression()

# Ejecutar la validación cruzada de 6 pliegues
# Pasamos el modelo, las características (X), el objetivo (y) y el objeto kf a cv
cv_scores = cross_val_score(reg, X, y, cv=kf)

# Imprimir los resultados de cada pliegue
print(cv_scores)
```

---

### Análisis de la Validación Cruzada de 6 pliegues

Al realizar este proceso, obtenemos una visión mucho más profunda del rendimiento del modelo que con un simple corte de datos.

- **Interpretación de `cv_scores`**: El resultado es un arreglo de seis números. Cada uno representa el coeficiente de determinación ($R^2$) obtenido en una de las seis iteraciones. Si los números son muy similares entre sí (por ejemplo, todos rondando el 0.75), el modelo es **robusto**. Si hay mucha variación (uno da 0.90 y otro 0.40), el modelo es **inestable** y depende demasiado de cómo se elijan los datos.
    
- **El objeto `KFold`**:
    
    - `n_splits=6`: Divide el dataset en 6 partes iguales.
        
    - `shuffle=True`: Es una buena práctica barajar los datos, especialmente si el dataset original tiene algún orden (por ejemplo, datos por fecha), para evitar que un pliegue se quede solo con datos de una tendencia específica.
        
    - `random_state=5`: Garantiza que, si otra persona corre el código, obtenga exactamente las mismas divisiones y resultados.
        
- **Importancia del $R^2$ en cada pliegue**: Al visualizar los seis puntajes, puedes detectar si existen subconjuntos de datos donde el modelo falla catastróficamente. Esto te ayuda a entender si la relación entre "redes sociales" y "ventas" es constante en todo el conjunto de datos o si hay anomalías que debas investigar.
    

---
Tras ejecutar la validación cruzada y obtener los puntajes individuales para cada pliegue (_fold_), el siguiente paso lógico es resumir esos datos para obtener conclusiones estadísticas sólidas. En este ejercicio, calcularemos la **media** para conocer el desempeño promedio, la **desviación típica** para medir la estabilidad del modelo y el **intervalo de confianza del 95%** para determinar el rango de precisión más probable.

```python
# Imprimir la media de los resultados (Mean)
# Representa el rendimiento promedio esperado del modelo
print(np.mean(cv_results))

# Imprimir la desviación típica (Standard Deviation)
# Mide qué tanto varían los resultados entre cada pliegue
print(np.std(cv_results))

# Visualizar el intervalo de confianza del 95%
# Usamos los cuantiles 0.025 y 0.975 para obtener el 95% central
print(np.quantile(cv_results, [0.025, 0.975]))
```

---

### Análisis de Métricas Estadísticas en ML

Cuando hablamos de validación cruzada, un solo número no cuenta la historia completa. Necesitamos entender la dispersión de los datos para confiar en el modelo.

#### 1. La Media ($\mu$)

Es el valor promedio de los coeficientes de determinación ($R^2$) obtenidos. Si tu media es de 0.75, puedes decir que, en promedio, tu modelo explica el 75% de la variabilidad de las ventas. Es nuestra mejor estimación del rendimiento real.

#### 2. La Desviación Típica ($\sigma$)

Esta métrica es el "termómetro" de la consistencia.

- **Baja desviación:** El modelo es estable; no importa cómo cortes los datos, siempre rinde igual.
    
- **Alta desviación:** El modelo es inestable o "suertudo"; su rendimiento cambia drásticamente dependiendo de los datos que le toquen para entrenar.
    

#### 3. Intervalo de Confianza del 95%

A diferencia de la media, que es un punto único, el intervalo de confianza nos da un **rango**.

- Al calcular `np.quantile(cv_results, [0.025, 0.975])`, estamos diciendo: "Tenemos un 95% de seguridad de que el $R^2$ de nuestro modelo cuando vea datos nuevos estará entre el valor A y el valor B".
    
- Esto es vital para presentar resultados a clientes o jefes, ya que muestra el nivel de incertidumbre del proyecto.
    

> 💡 **Tip de Pro:** Si tu desviación estándar es mayor a 0.1 o 0.15 en un problema de regresión, es una señal de alerta de que tu modelo podría estar sufriendo de alta varianza (sobreajuste) o que tu dataset es demasiado pequeño y poco representativo.
