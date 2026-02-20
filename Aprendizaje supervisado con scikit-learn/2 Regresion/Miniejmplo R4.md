La regresión **Ridge** es una técnica fundamental para controlar la complejidad de un modelo de regresión. Al añadir una penalización proporcional al cuadrado de los coeficientes, evitamos que el modelo se vuelva "demasiado sensible" a los datos de entrenamiento, protegiéndolo contra el sobreajuste. En este ejercicio, evaluaremos cómo impactan diferentes valores de **Alpha** ($\alpha$) en la capacidad de generalización del modelo utilizando el conjunto de datos `sales_df`.


```python
# Importar Ridge desde sklearn.linear_model
from sklearn.linear_model import Ridge

# Lista de valores alfa para evaluar el impacto de la regularización
alphas = [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]
ridge_scores = []

for alpha in alphas:
  
  # 1. Instanciar el modelo de regresión Ridge con el alfa actual
  ridge = Ridge(alpha=alpha)
  
  # 2. Ajustar el modelo a los datos de entrenamiento
  ridge.fit(X_train, y_train)
  
  # 3. Obtener el coeficiente de determinación R-cuadrado en el conjunto de prueba
  score = ridge.score(X_test, y_test)
  ridge_scores.append(score)

# Visualizar el rendimiento para cada nivel de penalización
print(ridge_scores)
```

---

### Análisis de la Regularización Ridge

El objetivo de este proceso es encontrar el "punto dulce" del hiperparámetro **Alpha**. Aquí te explico qué sucede técnicamente en cada paso del bucle:

#### La función de pérdida con penalización

A diferencia de la regresión lineal simple, Ridge intenta minimizar una función de pérdida que incluye un término adicional:

$$Loss = OLS + \alpha \sum_{i=1}^{n} a_i^2$$

Donde $a_i$ son los coeficientes de las características. Si los coeficientes crecen mucho, la pérdida aumenta drásticamente debido al cuadrado, obligando al modelo a mantener los pesos lo más pequeños posible.

#### El impacto de Alpha ($\alpha$)

- **Valores bajos (0.1, 1.0):** La penalización es ligera. El modelo se comporta casi como una regresión lineal estándar. Es útil si no hay mucho ruido en los datos.
    
- **Valores altos (1000.0, 10000.0):** La penalización es severa. El modelo se vuelve muy simple porque "aplasta" los coeficientes. Si el valor de `ridge_scores` empieza a bajar significativamente con alphas altos, significa que estamos cayendo en **ajuste insuficiente (underfitting)**.
    

#### Interpretación de los resultados

Al observar la lista `ridge_scores`, notarás que la precisión ($R^2$) cambia. El mejor valor de Alpha será aquel que proporcione el puntaje más alto en el conjunto de prueba. Este proceso de probar múltiples valores se conoce como **ajuste de hiperparámetros**, y es esencial porque no existe un valor de Alpha "mágico" que funcione para todos los datasets; siempre debe ser descubierto mediante experimentación.

---
La regresión **Lasso** (_Least Absolute Shrinkage and Selection Operator_) es una herramienta fascinante porque no solo ayuda a reducir el sobreajuste, sino que actúa como un "filtro inteligente". A diferencia de Ridge, Lasso tiene la propiedad matemática de reducir los coeficientes de las características menos importantes a **cero exactamente**, realizando así una selección automática de variables. En este ejercicio, utilizaremos Lasso con un $\alpha = 0.3$ sobre el dataset de ventas para identificar qué canales publicitarios realmente mueven la aguja.


```python
# Importar Lasso desde sklearn.linear_model
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt

# 1. Instanciar el modelo de regresión Lasso
# Usamos un alpha de 0.3 para controlar la fuerza de la penalización
lasso = Lasso(alpha=0.3)

# 2. Ajustar el modelo a los datos (X y y ya precargados)
lasso.fit(X, y)

# 3. Calcular y extraer los coeficientes del modelo
# El atributo .coef_ contiene la importancia asignada a cada variable
lasso_coef = lasso.coef_
print(lasso_coef)

# Visualización de la importancia de las características
plt.bar(sales_columns, lasso_coef)
plt.xticks(rotation=45)
plt.ylabel("Coeficientes de Lasso")
plt.title("Importancia de las características según Lasso")
plt.show()
```

---

### Análisis de Lasso y Selección de Características

Lasso es especialmente útil cuando tienes muchas características y sospechas que solo unas pocas son realmente relevantes.

#### La Función de Pérdida $L1$

La magia de Lasso reside en su penalización basada en el **valor absoluto** de los coeficientes. La función de pérdida que el modelo intenta minimizar es:

$$Loss = OLS + \alpha \sum_{j=1}^{p} |a_j|$$

Donde $|a_j|$ representa la magnitud absoluta de cada coeficiente. Debido a la forma geométrica de esta penalización, cuando el modelo intenta minimizar el error, tiende a "empujar" los coeficientes de las variables redundantes o poco informativas hasta que chocan con el **cero**.

#### Interpretación de los resultados

- **Coeficientes en Cero:** Si al graficar o imprimir `lasso_coef` ves que alguna columna tiene un valor de 0.0, significa que Lasso ha descartado esa característica por completo. El modelo considera que esa variable no aporta información útil para predecir las ventas una vez que las otras variables están presentes.
    
- **Coeficientes Distintos de Cero:** Las barras que permanecen visibles representan las variables críticas. La altura de la barra indica qué tanto impacto tiene esa inversión publicitaria específica en el aumento de las ventas.
    

#### Utilidad Práctica

Este método es oro puro para la toma de decisiones empresariales. En lugar de decir "todas las variables influyen un poco" (como haría una regresión estándar o Ridge), Lasso te permite decir: _"De todos nuestros gastos, solo la TV y el Radio tienen un impacto significativo; podemos ignorar el resto para simplificar nuestro análisis"_.
