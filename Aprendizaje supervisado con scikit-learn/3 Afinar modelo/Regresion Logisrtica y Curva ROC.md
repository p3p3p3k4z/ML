La **Regresión Logística** es, a pesar de su nombre, un algoritmo de **clasificación**, no de regresión. Es la piedra angular para entender cómo los modelos estiman probabilidades antes de tomar una decisión final.

Aquí tienes el apunte formal, mejorado y estructurado para tu colección de ingeniería.

---

## Regresión Logística y Evaluación con Curva ROC

### 1. ¿Qué es la Regresión Logística?

A diferencia de la regresión lineal que predice números continuos, la **Regresión Logística** calcula la **probabilidad ($p$)** de que una observación pertenezca a una clase específica (generalmente la clase positiva, "1").

- **Lógica de decisión:** El modelo aplica un umbral (threshold) por defecto de **0.5**.
    
    - Si $p \geq 0.5$, la etiqueta es **1** (ej. "Tiene diabetes").
        
    - Si $p < 0.5$, la etiqueta es **0** (ej. "No tiene diabetes").
        
- **Frontera de decisión:** Produce una **frontera de decisión lineal**, lo que significa que intenta separar las clases usando una línea recta (en 2D) o un plano (en 3D).
    

---

### 2. Predicción de Probabilidades

En Scikit-learn, además de usar `.predict()` para obtener el resultado final (0 o 1), podemos usar `.predict_proba()` para ver la confianza del modelo.


```python
# predict_proba devuelve dos columnas: [Probabilidad de 0, Probabilidad de 1]
y_pred_probs = logreg.predict_proba(X_test)[:, 1]

# Ejemplo de salida: 0.089 -> El modelo tiene un 8.9% de certeza de que es clase 1.
```

---

### 3. La Curva ROC (Receiver Operating Characteristic)

¿Qué pasa si 0.5 no es el mejor umbral? Para responder esto usamos la **Curva ROC**. Esta gráfica visualiza el rendimiento del modelo en **todos los umbrales posibles** (desde 0 hasta 1).

- **Eje Y (TPR - True Positive Rate):** También llamado _Recall_ o _Sensibilidad_. Es la capacidad de detectar los positivos reales.
    
- **Eje X (FPR - False Positive Rate):** La probabilidad de dar una falsa alarma (decir que es positivo cuando es negativo).
    

**Puntos clave de la curva:**

1. **Umbral = 0:** El modelo dice que "todos son 1". El TPR es 1 (detectas todo), pero el FPR también es 1 (fallas en todos los negativos).
    
2. **Umbral = 1:** El modelo dice que "nadie es 1". Ambos ratios son 0.
    
3. **Línea punteada:** Representa un modelo que "adivina al azar" (como lanzar una moneda). Queremos que nuestra curva esté lo más alejada posible de esta línea, hacia la esquina superior izquierda.
    

---

### 4. ROC AUC: El área bajo la curva

El **AUC (Area Under the Curve)** es la métrica que resume toda la curva ROC en un solo número.

- **Rango:** Va de **0 a 1**.
    
- **Interpretación:** * $AUC = 0.5$: El modelo no es mejor que el azar.
    
    - $AUC = 1.0$: El modelo es perfecto (detecta todos los positivos sin una sola falsa alarma).
        
    - $AUC = 0.67$: En el video, este modelo es un 34% mejor que el azar (calculado como $(0.67 - 0.5) / 0.5$).
        

---

### 5. Implementación en Scikit-learn

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

# 1. Ajustar el modelo
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

# 2. Obtener probabilidades de la clase positiva
y_pred_probs = logreg.predict_proba(X_test)[:, 1]

# 3. Calcular métricas de la curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_pred_probs)

# 4. Graficar
plt.plot([0, 1], [0, 1], 'k--') # Línea de azar
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()

# 5. Calcular el AUC Score
print("AUC Score: {}".format(roc_auc_score(y_test, y_pred_probs)))
```

---

### Resumen de Ingeniería

Como futuro **DevOps/SysAdmin**, entender el AUC es vital cuando monitoreas sistemas de alerta. Un AUC bajo en un sistema de detección de intrusiones significa que tu sistema te llenará de notificaciones basura o dejará pasar ataques reales.
