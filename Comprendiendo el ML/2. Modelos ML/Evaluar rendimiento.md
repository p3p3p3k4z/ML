Una vez que un modelo está entrenado, es crucial evaluar qué tan bien funciona. Para esto, se utiliza el **conjunto de prueba**, que contiene datos que el modelo nunca ha visto.

---

### El Desafío Principal: Sobreajuste (Overfitting)

El objetivo principal de la evaluación es detectar el sobreajuste.

- **Definición:** Un modelo está sobreajustado cuando **funciona muy bien con los datos de entrenamiento**, pero **funciona mal con los datos de prueba**.
    
- **Causa:** El modelo **"memoriza" los detalles y el ruido de los datos de entrenamiento** en lugar de aprender el patrón general.
    
- **Consecuencia:** El modelo **no puede generalizar lo que aprende** para hacer predicciones correctas sobre datos nuevos.
    

---

### Métricas para Clasificación

#### Exactitud (Accuracy)

- **Definición:** Es la métrica más simple. Mide el porcentaje de **observaciones clasificadas correctamente** del total de **todas las observaciones**.
    
- **Fórmula:** $Exactitud = \frac{\text{Predicciones Correctas}}{\text{Total de Observaciones}}$
    
- **Límites de la Exactitud:** Esta métrica puede ser muy engañosa en conjuntos de datos desbalanceados.
    
    - **Ejemplo de Fraude:** Si solo el 1% de las **transacciones son fraudulentas**, un modelo que _siempre_ prediga "No Fraude" tendrá un 99% de exactitud, pero será un modelo inútil, pues no detecta ningún fraude.
        

#### Matriz de Confusión

Para solucionar los límites de la exactitud, se usa una Matriz de Confusión, que desglosa los aciertos y errores.

||**Predicho: Positivo**|**Predicho: Negativo**|
|---|---|---|
|**Real: Positivo**|Verdaderos Positivos (TP)|**Falsos Negativos (FN)**|
|**Real: Negativo**|Falsos Positivos (FP)|Verdaderos Negativos (TN)|

- **Verdaderos Positivos (TP):** Predijo "Positivo" y era "Positivo". (Acierto)
    
- **Verdaderos Negativos (TN):** Predijo "Negativo" y era "Negativo". (Acierto)
    
- **Falsos Positivos (FP):** Predijo "Positivo", pero era "Negativo". (Error Tipo I)
    
- **Falsos Negativos (FN):** Predijo "Negativo", pero era "Positivo". (Error Tipo II - A menudo el error más costoso, ej. no detectar un fraude).
    

A partir de esta matriz se derivan métricas más robustas:

- **Sensibilidad (Recall):** Mide qué tan bien el modelo encuentra _todos los positivos_.
    
    - $Sensibilidad = \frac{TP}{TP + FN}$
        
- **Especificidad:** Mide qué tan bien el modelo encuentra _todos los negativos_.
    
    - $Especificidad = \frac{TN}{TN + FP}$
        
- **Precisión (Precision):** De las veces que el modelo predijo "Positivo", ¿cuántas veces acertó?
    
    - $Precisión = \frac{TP}{TP + FP}$
        

---

### Métricas para Regresión

En regresión no medimos "correcto/incorrecto", sino _qué tan cerca_ está la predicción del valor real.

- **Error Cuadrático Medio (MSE - Mean Squared Error):** Es el promedio de los errores al cuadrado. Penaliza más los errores grandes.
    
    - $MSE = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$
        
- **Raíz del Error Cuadrático Medio (RMSE):** Es la raíz cuadrada del MSE. Es muy útil porque el error se expresa en las mismas unidades que la variable objetivo (ej. "el modelo se equivoca en promedio por $5,000").
    

---

### Conclusión: La Métrica Depende del Objetivo

En el **aprendizaje supervisado** (y en general), la métrica de rendimiento que se elige **depende del problema y de los objetivos del negocio**.

- Evaluar el rendimiento no es solo ver un número.
    
- Es entender _qué tipo de error_ es más costoso (ej. un Falso Negativo en un diagnóstico médico es mucho peor que un Falso Positivo).