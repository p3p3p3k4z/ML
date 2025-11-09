## Regularización: Evitando el Sobreajuste 🛡️

La **regularización** es una técnica fundamental en Machine Learning para crear modelos más robustos y generalizables, especialmente cuando se trabaja con muchas características. Su objetivo es evitar que el modelo se vuelva demasiado complejo y se "memorice" los datos de entrenamiento (sobreajuste).

-----

### El Problema de la Complejidad: ¿Por qué Regularizar?

En la regresión lineal, el modelo intenta encontrar un **coeficiente** (peso) óptimo para cada característica (columna) de tus datos. Estos coeficientes cuantifican el efecto de cada característica en la predicción.

  * **Más características = Más coeficientes.**
  * **Escenario Ideal:** Tienes muchas filas (datos) y pocas columnas (características). Aquí, la regresión estándar funciona bien.
  * **Escenario Problemático:** Tienes **muchas columnas** y pocas filas. El modelo tiene demasiada libertad y puede encontrar relaciones espurias (ruido) que solo existen en esos datos específicos. Esto lleva a un modelo complejo, difícil de interpretar y que falla con datos nuevos.

**El Objetivo:** Buscamos un modelo **parsimonioso**, es decir, lo más simple posible pero que aún haga buenas predicciones. Queremos seleccionar automáticamente el subconjunto de características que realmente importan.

-----

### La Solución: Regresión Penalizada

La regularización funciona modificando la **función de pérdida** que el algoritmo intenta minimizar durante el entrenamiento.

  * **Función de Pérdida Estándar (MSE):** Solo se preocupa por minimizar el error de predicción.
      * $Pérdida = MSE$
  * **Función de Pérdida Regularizada:** Añade un **término de penalización** que "castiga" al modelo por tener coeficientes grandes.
      * $Pérdida = MSE + \lambda \cdot Penalización$

Donde $\lambda$ (lambda, o `regParam` en Spark) controla la fuerza de la penalización:

  * Si $\lambda = 0$, no hay regularización (es regresión estándar).
  * Si $\lambda$ es muy grande, la penalización domina y fuerza a los coeficientes a ser muy pequeños (o cero).

-----

### Tipos de Regularización: Ridge y Lasso

Existen dos formas principales de definir este término de penalización, que tienen efectos diferentes en los coeficientes. En Spark, se controlan con `elasticNetParam`.

#### 1\. Regresión Ridge (Norma L2)

  * **Penalización:** Se basa en la suma de los **cuadrados** de los coeficientes ($\sum \beta_i^2$).
  * **Efecto:** Reduce **todos** los coeficientes hacia cero de manera proporcional, pero raramente los hace exactamente cero.
  * **Uso:** Ideal cuando crees que **muchas características contribuyen un poco** al resultado final.
  * **En Spark:** `elasticNetParam = 0.0`.

<!-- end list -->

```python
# Ridge Regression en Spark
# elasticNetParam=0.0 indica Ridge. regParam=0.1 es la fuerza de la penalización.
ridge = LinearRegression(labelCol='consumption', elasticNetParam=0.0, regParam=0.1)
ridge_model = ridge.fit(cars_train)

# Examinar coeficientes: Serán más pequeños que sin regularización, pero no cero.
print(ridge_model.coefficients)
```

#### 2\. Regresión Lasso (Norma L1)

  * **Penalización:** Se basa en la suma de los **valores absolutos** de los coeficientes ($\sum |\beta_i|$).
  * **Efecto:** Tiene la propiedad única de poder reducir algunos coeficientes **exactamente a cero**.
  * **Uso:** Funciona como una **selección automática de características**. Es ideal cuando crees que solo un **pequeño subconjunto de características** es realmente importante y quieres ignorar el resto (modelo parsimonioso).
  * **En Spark:** `elasticNetParam = 1.0`.

<!-- end list -->

```python
# Lasso Regression en Spark
# elasticNetParam=1.0 indica Lasso.
lasso = LinearRegression(labelCol='consumption', elasticNetParam=1.0, regParam=0.1)
lasso_model = lasso.fit(cars_train)

# Examinar coeficientes: Verás varios valores de 0.0, indicando características eliminadas.
print(lasso_model.coefficients)
```

#### 3\. Elastic Net

  * Es un compromiso entre ambas. Combina las penalizaciones L1 y L2.
  * **En Spark:** `elasticNetParam` puede ser cualquier valor entre 0.0 y 1.0 (ej. 0.5 para una mezcla 50/50).

-----

### Resumen de Parámetros Clave en Spark ML

| Parámetro | Nombre Matemático | Significado | Valores Típicos |
| :--- | :---: | :--- | :--- |
| `regParam` | $\lambda$ (Lambda) | **Fuerza** de la regularización. | $\ge 0$. (Ej. 0.01, 0.1, 1.0). Se debe ajustar con validación cruzada. |
| `elasticNetParam` | $\alpha$ (Alpha) | **Tipo** de mezcla de regularización. | 0.0 (Ridge), 1.0 (Lasso), o intermedio (Elastic Net). |