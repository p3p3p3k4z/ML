## Validación Cruzada (Cross-Validation)

Hasta ahora, hemos medido el rendimiento con un solo conjunto de prueba. Sin embargo, el valor de $R^2$ resultante depende totalmente de cómo se dividieron los datos aleatoriamente. Si el conjunto de prueba tiene datos "fáciles", el modelo parecerá mejor de lo que es; si tiene datos atípicos, parecerá peor. Para solucionar esta dependencia, utilizamos la técnica de **k-fold Cross-Validation**.


El objetivo es implementar una validación cruzada de 6 pliegues (6-fold CV) para evaluar la estabilidad de un modelo de regresión lineal sobre el conjunto de datos de ventas. Para asegurar que el proceso sea robusto, se deben barajar los datos antes de dividirlos y calcular no solo el promedio de los resultados, sino también su desviación estándar y el intervalo de confianza del 95%.

```python
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression

# 1. Configurar el esquema de validación (KFold)
# Usamos shuffle=True para evitar sesgos si los datos están ordenados
kf = KFold(n_splits=6, shuffle=True, random_state=42)

# 2. Instanciar el modelo
reg = LinearRegression()

# 3. Ejecutar la validación cruzada
# Por defecto, devuelve R-cuadrado para regresión lineal
cv_results = cross_val_score(reg, X, y, cv=kf)

# 4. Evaluación estadística de los resultados
print("Resultados de cada pliegue:", cv_results)
print("Media de R^2: {}".format(np.mean(cv_results)))
print("Desviación estándar: {}".format(np.std(cv_results)))

# 5. Calcular el intervalo de confianza del 95%
print("Intervalo de confianza (95%):", np.quantile(cv_results, [0.025, 0.975]))
```

---

### Fundamentos y Complementos Técnicos

#### ¿Cómo funciona el proceso de "Folds"?

Imagina que divides tus datos en 5 grupos ($k=5$):

1. **Iteración 1:** El grupo 1 es el examen (test), los grupos 2, 3, 4 y 5 son el estudio (entrenamiento).
    
2. **Iteración 2:** El grupo 2 es el examen, los demás son el estudio.
    
3. **... así sucesivamente** hasta que todos los grupos hayan sido "el examen" una vez.
    

Al final, no tienes un solo $R^2$, tienes 5. Esto te permite ver qué tanto **varía** el rendimiento del modelo dependiendo de los datos que vea.

#### El Compromiso (Trade-off) de $k$

- **$k$ alto (ej. 10 o más):** El modelo es evaluado de forma más exhaustiva, pero el costo computacional aumenta drásticamente (tienes que entrenar el modelo 10 veces).
    
- **$k$ bajo (ej. 5):** Es más rápido, pero existe un ligero riesgo de que los resultados sigan siendo un poco dependientes de la suerte del split.
    

#### Estadísticas Críticas

- **Media (Mean):** Es tu "verdadera" métrica de rendimiento.
    
- **Desviación Estándar (Std):** Mide la **consistencia**. Si la media es 0.80 pero la desviación es 0.20, tu modelo es inestable (a veces es excelente y a veces falla). Queremos una desviación estándar lo más pequeña posible.
    
- **Intervalo de Confianza:** Nos dice que, con un 95% de seguridad, el rendimiento del modelo en el mundo real estará entre esos dos valores (límite inferior y superior).
    

> 💡 **Analogía del Estudiante:** La validación cruzada es como hacer 5 exámenes parciales diferentes a lo largo del semestre en lugar de jugarse toda la nota en un solo examen final. El promedio de esos 5 exámenes refleja mucho mejor tu conocimiento real que una sola prueba donde podrías haber estado nervioso o haber tenido suerte con las preguntas.
