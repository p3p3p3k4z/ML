La regresión es el otro gran pilar del aprendizaje supervisado. Mientras que en la clasificación buscábamos etiquetas (¿es perro o gato?), en la regresión buscamos **predecir números dentro de un rango continuo**.

Aquí tienes tu apunte refinado, enriquecido con analogías y los detalles técnicos que vimos en el video.

---

## Introducción a la Regresión

La regresión es la tarea de predecir un valor numérico específico. A diferencia de la clasificación, donde los resultados son categorías discretas, en la regresión los resultados pueden ser **infinitos** dentro de una escala.

### Definición y Características

**Definición:** Es un proceso estadístico y de ML que estima las relaciones entre variables. Se utiliza para predecir una **variable objetivo (target)** continua basándose en una o más **características (features)**.

**Características principales:**

- **Continuidad:** El valor de salida es un número real (ej. 15.5, 100.2, 1000.0).
    
- **Correlación:** Busca entender cómo cambia la variable objetivo cuando una característica se mueve (ej. si el IMC sube, ¿sube la glucosa?).
    
- **Línea de mejor ajuste (Line of Best Fit):** El objetivo matemático es trazar una línea que pase lo más cerca posible de todos los puntos de datos.
    

---

### Ejemplos del Mundo Real

- **Economía:** Predecir el PIB (Producto Interno Bruto) de un país.
    
- **Bienes Raíces:** Estimar el precio de una casa según sus metros cuadrados y ubicación.
    
- **Salud (Caso de estudio):** Predecir los niveles de **glucosa en sangre** basándose en el Índice de Masa Corporal (IMC).
    

---

### Preparación de Datos: El reto del Array 2D

En el video vimos que `scikit-learn` es muy exigente con la forma de los datos, especialmente cuando usamos una **sola característica** (regresión univariada).

#### El problema de la dimensión

Si extraemos una sola columna (como el IMC), Python nos da un array de una dimensión (1D). Pero `scikit-learn` siempre espera que $X$ sea una matriz (2D).

#### La solución: `.reshape()`

Para convertir un array de una lista simple a una "columna de tabla", usamos NumPy:


```python
# -1 significa "mantén todas las filas", 1 significa "hazlo una sola columna"
X_bmi = X_bmi.reshape(-1, 1)
```

---

### Flujo de Trabajo: Regresión Lineal

La **Regresión Lineal** es el algoritmo más básico. Intenta ajustar una línea recta a los datos siguiendo la ecuación:

$$y = ax + b$$

Donde **$a$** es la pendiente (qué tanto afecta la $X$ a la $y$) y **$b$** es la intersección (dónde corta el eje vertical).

#### Pasos en código:

1. **Importar:** `from sklearn.linear_model import LinearRegression`
    
2. **Instanciar:** `reg = LinearRegression()`
    
3. **Ajustar (Fit):** `reg.fit(X_bmi, y)` (Aquí el modelo encuentra los valores óptimos de $a$ y $b$).
    
4. **Predecir:** `predictions = reg.predict(X_bmi)`
    

### Visualización de resultados

Al graficar, verás dos capas:

1. **Scatter plot:** Los puntos reales de los pacientes.
    
2. **Line plot:** La línea negra que representa la predicción del modelo.
    

Si la línea sube hacia la derecha, tenemos una **correlación positiva**: a mayor IMC, mayor nivel de glucosa esperado.
Tienes razón, vamos a aterrizar los detalles técnicos y el flujo de código que se presentó en el video para que tu apunte sea totalmente funcional. Aquí tienes la continuación centrada en la implementación con **scikit-learn** y **NumPy**.

---

## Implementación de Regresión Lineal

En este ejemplo, el objetivo es predecir los niveles de glucosa en sangre utilizando el Índice de Masa Corporal (IMC o BMI) como característica principal.

### Preparación de las Matrices: X e y

Para trabajar con scikit-learn, debemos separar los datos en dos variables distintas. Una convención común en Python es usar los atributos de **Pandas** y convertirlos a arreglos de **NumPy**.

- **Crear X (Características):** Eliminamos la columna objetivo del DataFrame original.
    
- **Crear y (Objetivo):** Seleccionamos únicamente la columna que queremos predecir.
    

```python
# Eliminamos la columna 'glucose' para dejar solo las características
X = diabetes_df.drop("glucose", axis=1).values

# Seleccionamos solo la columna 'glucose' como nuestro objetivo
y = diabetes_df["glucose"].values
```

### El Reto de la Dimensión: Reshape de X

Cuando realizamos una regresión con **una sola característica** (como solo el IMC), scikit-learn requiere que esa columna se comporte como una matriz (2D), no como una lista simple (1D).

Si tomamos la columna 4 de nuestra matriz $X$ (que corresponde al IMC):

```python
import numpy as np

# Extraemos la columna del IMC
X_bmi = X[:, 3] 

# El truco del Reshape
# -1 le dice a NumPy: "calcula tú el número de filas"
# 1 le dice: "pero déjame solo una columna"
X_bmi = X_bmi.reshape(-1, 1)

print(X_bmi.shape) # Resultado esperado: (N, 1)
```

> 💡 **Analogía del estante:** Imagina que tienes una fila de libros en el suelo (1D). Scikit-learn es un estante que solo acepta cajas. El `reshape` es como meter cada libro en una caja individual y apilarlas una sobre otra para que ahora tengan una estructura de "columna" (2D).

---

### Ajuste y Predicción del Modelo

Una vez que los datos tienen la forma correcta, seguimos el flujo estándar de `sklearn`.


```python
from sklearn.linear_model import LinearRegression

# 1. Instanciar el modelo
reg = LinearRegression()

# 2. Ajustar (Entrenar) el modelo con los datos
# Aquí el modelo busca la línea que mejor se adapta a los puntos
reg.fit(X_bmi, y)

# 3. Realizar predicciones
# Usamos los mismos datos de X para ver dónde queda la línea de ajuste
predictions = reg.predict(X_bmi)
```

### Visualización del Modelo

Para entender visualmente qué hizo el modelo, superponemos los datos reales con la línea de predicción.

```python
import matplotlib.pyplot as plt

# Graficamos los puntos reales (Dispersión)
plt.scatter(X_bmi, y, color="blue", alpha=0.5)

# Graficamos la línea de predicción (Regresión)
plt.plot(X_bmi, predictions, color="black", linewidth=3)

plt.xlabel("Índice de Masa Corporal (BMI)")
plt.ylabel("Glucosa en Sangre")
plt.show()
```

### Interpretación de la Gráfica

- **Los puntos azules:** Representan a cada paciente real. Notarás que hay mucha dispersión; esto es normal en datos biológicos.
    
- **La línea negra:** Es la **Línea de Mejor Ajuste**. Representa la tendencia general.
    
- **Conclusión visual:** Existe una **correlación positiva débil a moderada**. Esto significa que, estadísticamente, a medida que aumenta el IMC, los niveles de glucosa en sangre tienden a subir, aunque no de forma exacta para todos los individuos.
    