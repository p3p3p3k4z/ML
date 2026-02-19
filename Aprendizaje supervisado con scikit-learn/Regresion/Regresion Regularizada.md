La **regularización** es una de las técnicas más potentes para rescatar a un modelo de las garras del **sobreajuste (overfitting)**. Si la regresión lineal estándar es un estudiante que intenta memorizar cada punto de los datos, la regularización es el tutor que le dice: "Céntrate en lo importante y no te compliques demasiado con los detalles irrelevantes".

---

## Regresión Regularizada: Ridge y Lasso

### ¿Por qué regularizar?

En una regresión lineal estándar (OLS), el modelo intenta minimizar la función de pérdida eligiendo coeficientes ($a$) para cada característica. Si permitimos que estos coeficientes crezcan sin control, el modelo se vuelve demasiado sensible al ruido de los datos de entrenamiento, lo que causa sobreajuste.

La regularización **penaliza los coeficientes grandes** modificando la función de pérdida. Es como ponerle un "impuesto" a la complejidad del modelo.

---

### Regresión Ridge

La Regresión Ridge añade a la función de pérdida el cuadrado de los coeficientes multiplicado por una constante llamada **Alpha ($\alpha$)**.

- **Alpha ($\alpha$):** Es un hiperparámetro que controla la complejidad.
    
    - **$\alpha = 0$:** Es una regresión lineal normal (peligro de sobreajuste).
        
    - **$\alpha$ muy alto:** Penaliza tanto los coeficientes que pueden terminar siendo casi cero, provocando **ajuste insuficiente (underfitting)**.
        

> 💡 **Analogía del equipaje:** Imagina que vas de viaje (entrenar el modelo). OLS es llevar todas las maletas que quieras. Ridge es una aerolínea que te cobra por el **cuadrado del peso** de cada maleta. Intentarás llevar solo lo necesario y que nada sea excesivamente pesado para no pagar una fortuna.


```python
from sklearn.linear_model import Ridge

# Crear lista para guardar puntuaciones
scores = []

# Probar diferentes alphas
for alpha in [0.1, 1.0, 10.0, 100.0, 1000.0]:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train, y_train)
    
    # Evaluar el rendimiento (R-cuadrado)
    score = ridge.score(X_test, y_test)
    scores.append(score)

print(scores)
```

---

### Regresión Lasso

Lasso (_Least Absolute Shrinkage and Selection Operator_) funciona de forma similar a Ridge, pero en lugar de usar el cuadrado de los coeficientes, utiliza su **valor absoluto**.

- **Diferencia clave:** Mientras que Ridge reduce los coeficientes pero rara vez los hace cero, Lasso tiene la capacidad de **reducir coeficientes a cero exactamente**.
    

#### Lasso para la Selección de Características

Debido a que Lasso puede eliminar características (poniendo su coeficiente en 0), es una herramienta increíble para identificar qué variables son realmente importantes y cuáles son solo "ruido".

#### Código y Visualización de Importancia

Python

```
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt

# Obtener los nombres de las columnas
names = sales_df.drop("sales", axis=1).columns

# Instanciar Lasso con un alpha pequeño
lasso = Lasso(alpha=0.1)

# Ajustar a TODOS los datos para ver importancia
lasso.fit(X, y)

# Extraer los coeficientes
lasso_coef = lasso.coef_

# Graficar la importancia de cada característica
plt.plot(range(len(names)), lasso_coef)
plt.xticks(range(len(names)), names, rotation=60)
plt.ylabel("Coeficientes")
plt.show()
```

---

### Explicación del Gráfico de Lasso

Al ejecutar el código anterior, verás un gráfico con picos y valles:

- **Picos altos (positivos o negativos):** Representan las características que más influyen en el resultado (ej. en el caso de la glucosa, el factor "diabetes" tendrá un coeficiente muy alto).
    
- **Línea en cero:** Son las características que Lasso "descartó". El modelo decidió que no aportan información útil para la predicción.
    

**Beneficios de Lasso:**

1. **Claridad:** Permite explicar resultados a audiencias no técnicas ("Estas 3 variables son las que mueven el negocio").
    
2. **Eficiencia:** Reduce la cantidad de datos necesarios para futuras predicciones al ignorar lo irrelevante.
    

¿Te gustaría que hagamos un ejercicio práctico para comparar los coeficientes de una Regresión Lineal normal frente a una de Lasso y ver cuántas variables "mueren" en el proceso?