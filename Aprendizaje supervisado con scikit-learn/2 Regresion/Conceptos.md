# Regresión Lineal y Mínimos Cuadrados Ordinarios (OLS)

## 1. Fundamentos Matemáticos

La regresión lineal busca modelar la relación entre una variable dependiente (objetivo) y una o más variables independientes (características).

- **Regresión Lineal Simple:** Se usa una sola característica ($x$).
    
    - **Ecuación:** $y = ax + b$
        
- **Regresión Lineal Múltiple:** Se usan $n$ características.
    
    - **Ecuación:** $y = a_1x_1 + a_2x_2 + ... + a_nx_n + b$
        

### Componentes Clave:

- **$y$ (Target):** La variable que queremos predecir.
    
- **$x$ (Feature):** El dato de entrada.
    
- **$a$ (Coeficientes/Pendiente):** Determinan cuánto cambia $y$ por cada unidad de cambio en $x$.
    
- **$b$ (Intercepto):** El valor de $y$ cuando todas las $x$ son cero.
    

---

## 2. El Proceso de Optimización (Mecánica)

Para encontrar la "mejor línea", necesitamos medir qué tan lejos están nuestras predicciones de la realidad.

- **Residual (Residuo):** Es la distancia vertical entre un punto de dato real y la línea de predicción.
    
- **Función de Pérdida (Loss Function):** Una fórmula que cuantifica el error total del modelo. En regresión, la más común es el **RSS** (Suma de los Cuadrados de los Residuos).
    

### ¿Por qué elevar al cuadrado?

Si solo sumamos las distancias, los errores positivos (puntos arriba de la línea) se cancelarían con los negativos (puntos abajo), dando un error total de cero en una línea claramente errónea. Al elevar al cuadrado, todos los errores se vuelven positivos y penalizamos más los errores grandes.

> **Mínimos Cuadrados Ordinarios (OLS):** Es el método que busca los valores de $a$ y $b$ que **minimizan** el RSS.

---

## 3. Implementación en Scikit-Learn

En Python, el flujo de trabajo para una regresión múltiple sigue un estándar claro:

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 1. Preparar datos (X debe ser 2D, y debe ser 1D)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. Instanciar y Entrenar
reg = LinearRegression() 
reg.fit(X_train, y_train) # Aquí ocurre el OLS internamente

# 3. Predecir
y_pred = reg.predict(X_test)
```

---

## 4. Métricas de Evaluación

¿Qué tan bueno es nuestro modelo? Usamos tres métricas principales:

|**Métrica**|**Definición**|**Interpretación**|
|---|---|---|
|**$R^2$ (R-cuadrado)**|Proporción de la varianza del target explicada por el modelo.|**0 a 1**. 1 es ajuste perfecto, 0 es un modelo que solo predice el promedio.|
|**MSE** (Error Cuadrático Medio)|Promedio de los residuos al cuadrado.|Difícil de leer porque las unidades están al cuadrado (ej: dólares$^2$).|
|**RMSE** (Raíz del MSE)|Raíz cuadrada del MSE.|**Muy útil**. Está en las mismas unidades que el target (ej: dólares).|

```python
from sklearn.metrics import root_mean_squared_error

# R-cuadrado
r_squared = reg.score(X_test, y_test)

# RMSE
rmse = root_mean_squared_error(y_test, y_pred)
```

---

## Resumen para recordar:

1. **OLS** es el "motor" que minimiza la distancia al cuadrado entre los puntos y la línea.
    
2. **Scikit-learn** hace todo el cálculo de OLS automáticamente al llamar a `.fit()`.
    
3. Usa **$R^2$** para saber qué tan "explicativo" es tu modelo y **RMSE** para saber cuánto se equivoca en promedio en la unidad de medida real.
    
