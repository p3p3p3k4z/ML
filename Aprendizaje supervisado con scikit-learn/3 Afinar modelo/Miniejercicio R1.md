Utilizaremos el conjunto de datos `diabetes_df` para construir un modelo de **Regresión Logística**. A diferencia de los modelos previos que devuelven una clase directa (0 o 1), aquí nos enfocaremos en obtener la **probabilidad** de pertenencia a la clase positiva. Esto es fundamental en contextos médicos, donde conocer la certeza del diagnóstico es tan importante como el diagnóstico mismo. El conjunto de datos ya ha sido dividido en `X_train`, `X_test`, `y_train` e `y_test`.


```python
# Importar LogisticRegression
from sklearn.linear_model import LogisticRegression

# Instanciar el modelo de regresión logística
logreg = LogisticRegression()

# Ajustar el modelo a los datos de entrenamiento
logreg.fit(X_train, y_train)

# Predecir probabilidades para el conjunto de prueba
# Seleccionamos la segunda columna [:, 1] que corresponde a la clase positiva (diabetes)
y_pred_probs = logreg.predict_proba(X_test)[:, 1]

# Visualizar las primeras diez probabilidades estimadas
print(y_pred_probs[:10])
```

---

### Análisis de la Predicción de Probabilidades

En este paso, hemos pasado de una clasificación "rígida" a una "probabilística". Aquí te explico los detalles técnicos clave para tu formación como ingeniero:

- **`predict_proba` vs `predict`**: Mientras que `.predict()` te daría un 0 o un 1 basándose en el umbral por defecto (0.5), `.predict_proba()` te devuelve una matriz con dos columnas. La primera es la probabilidad de ser clase 0 y la segunda la de ser clase 1.
    
- **Slicing `[:, 1]`**: En Python, esta nomenclatura es vital. Le indicamos al modelo: "toma todas las filas (`:`) pero quédate únicamente con la segunda columna (`1`)". Esa columna representa la probabilidad de que el paciente **sí tenga diabetes**.
    
- **Utilidad en Producción**: Como aspirante a **DevOps**, piensa en esto como un sistema de _logging_ de criticidad. No es lo mismo una alerta con un 51% de probabilidad que una con un 99%. Obtener las probabilidades te permite crear sistemas de triaje donde los casos con mayor probabilidad se atiendan con mayor prioridad.
    

Al observar la salida de `print(y_pred_probs[:10])`, verás valores entre 0 y 1 (ej. `0.12`, `0.85`). Un `0.85` significa que el modelo tiene un 85% de confianza en que esa observación pertenece a la clase positiva.

---
Una vez construido el modelo de regresión logística para predecir el estado diabético, el siguiente paso crítico es evaluar su desempeño en todos los umbrales de decisión posibles. La **Curva ROC** permite visualizar la relación entre la tasa de verdaderos positivos (sensibilidad) y la tasa de falsos positivos (1 - especificidad). El objetivo es observar qué tan lejos se encuentra nuestra curva de la línea de azar (la línea punteada), lo cual indica la capacidad discriminatoria del modelo.

```python
# Importar roc_curve desde sklearn.metrics
from sklearn.metrics import roc_curve

# Generar los valores de la curva ROC: fpr, tpr, thresholds
# Pasamos las etiquetas reales y las probabilidades de la clase positiva
fpr, tpr, thresholds = roc_curve(y_test, y_pred_probs)

# Dibujar la línea punteada que representa un modelo aleatorio (base)
plt.plot([0, 1], [0, 1], 'k--')

# Graficar la tasa de verdaderos positivos (tpr) frente a la de falsos positivos (fpr)
plt.plot(fpr, tpr)

# Configuración de etiquetas y título
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Diabetes Prediction')

# Mostrar el gráfico
plt.show()
```

---

### Análisis de la Curva ROC

La Curva ROC es una de las herramientas de diagnóstico más potentes en el aprendizaje supervisado. Aquí te detallo los puntos clave para interpretarla como un experto:

#### 1. Los Ejes: TPR y FPR

- **True Positive Rate (TPR):** También conocido como _Recall_ o Sensibilidad. Representa la proporción de individuos con diabetes que el modelo identificó correctamente.
    
- **False Positive Rate (FPR):** Es la proporción de individuos sanos que el modelo clasificó erróneamente como diabéticos. Queremos que este valor sea lo más bajo posible.
    

#### 2. La Línea Punteada ($y = x$)

Esta línea representa un modelo que no tiene capacidad predictiva, es decir, un modelo que adivina al azar (como lanzar una moneda). Cualquier modelo útil debe tener una curva que se sitúe **por encima** de esta línea.

#### 3. El "Codo" de la Curva

El objetivo ideal es que la curva se acerque lo más posible a la **esquina superior izquierda** del gráfico. Ese punto representa un escenario con un TPR de 1.0 (detectamos a todos los enfermos) y un FPR de 0.0 (no damos falsas alarmas).

- **Punto de equilibrio:** Al observar la curva, puedes elegir un umbral específico que equilibre el costo de un falso positivo frente al riesgo de un falso negativo. En medicina, a menudo aceptamos un FPR ligeramente más alto si eso nos garantiza un TPR (detección) cercano al 100%.
    

#### 4. Relación con el AUC

Aunque este ejercicio se centra en la visualización, recuerda que el área total debajo de esta línea azul es el **AUC**. Cuanto más "abombada" esté la curva hacia arriba, mayor será el área y, por lo tanto, mejor será el modelo para distinguir entre las dos clases.

---
Tras haber visualizado la curva ROC, el paso final es cuantificar esa capacidad de discriminación mediante la métrica **AUC** (_Area Under the Curve_). En este ejercicio, calcularemos el área bajo la curva para el modelo de regresión logística y lo compararemos con la matriz de confusión y el reporte de clasificación. Esto nos permitirá tener una visión de $360^{\circ}$ sobre qué tan bien el modelo separa a los individuos sanos de los diabéticos en comparación con otros modelos como KNN.


```python
# Importar roc_auc_score desde sklearn.metrics
from sklearn.metrics import roc_auc_score

# 1. Calcular e imprimir la puntuación ROC AUC
# Pasamos las etiquetas reales y las probabilidades de la clase positiva
print(roc_auc_score(y_test, y_pred_probs))

# 2. Calcular e imprimir la matriz de confusión
# Comparamos etiquetas reales con las etiquetas predichas (0 o 1)
print(confusion_matrix(y_test, y_pred))

# 3. Calcular e imprimir el informe de clasificación
print(classification_report(y_test, y_pred))
```

---

### Análisis Integral de Métricas

Para un ingeniero de datos o un especialista en modelos predictivos, el AUC es la "prueba de fuego" de la robustez de un clasificador binario.

#### 1. ¿Qué nos dice el ROC AUC Score?

El valor del AUC representa la probabilidad de que el modelo asigne una probabilidad más alta a un caso positivo elegido al azar que a un caso negativo elegido al azar.

- **$AUC = 0.5$**: El modelo no tiene capacidad de discriminación (es como lanzar una moneda).
    
- **$0.7 \leq AUC < 0.8$**: Se considera una capacidad aceptable.
    
- **$0.8 \leq AUC < 0.9$**: Se considera una capacidad excelente.
    
- **$AUC \geq 0.9$**: Es una capacidad excepcional.
    

#### 2. La Triangulación: AUC, Matriz e Informe

- **El AUC** te da una métrica global de la capacidad del modelo para "ordenar" las observaciones por probabilidad, independientemente del umbral.
    
- **La Matriz de Confusión** te muestra exactamente dónde está fallando el modelo (¿estamos dejando ir a muchos diabéticos o estamos asustando a gente sana?).
    
- **El Informe de Clasificación** te da el detalle de **Precision** (calidad) y **Recall** (cantidad) para cada clase.
    

#### 3. Comparativa de Modelos

En este ejercicio, al comparar los resultados de la **Regresión Logística** contra los de **KNN**, notarás que uno suele tener un AUC más alto. Generalmente, la Regresión Logística es muy robusta para problemas médicos porque su naturaleza probabilística se adapta mejor a la variabilidad de los datos biológicos que la votación por cercanía de KNN.

> 💡 **Nota Técnica:** El AUC es especialmente valioso cuando tienes un **desequilibrio de clases**, ya que no se ve tan afectado por el tamaño de las clases como la métrica de _Accuracy_.
