## Creación de Características (Preprocesamiento)

Trabajaremos con el conjunto de datos `sales_df`, que contiene el gasto en campañas publicitarias (TV, radio, redes sociales) y las ventas generadas. El objetivo es utilizar la inversión en **"radio"** como característica para predecir las **"sales"** (ventas).

Antes de entrenar el modelo, es imperativo procesar los datos para que cumplan con los requisitos de scikit-learn:

1. Extraer las columnas necesarias.
    
2. Convertirlas a arreglos de NumPy.
    
3. Asegurar que la matriz de características ($X$) sea bidimensional (2D).
    

```python
import numpy as np

# 1. Extraer la columna de características (radio) y el objetivo (sales)
# Usamos .values para obtener arrays de NumPy directamente
X = sales_df["radio"].values
y = sales_df["sales"].values

# 2. Remodelar X a una matriz bidimensional
# Scikit-learn no acepta arrays 1D para las características (X)
X = X.reshape(-1, 1)

# 3. Verificar las dimensiones de los datos preparados
print("Forma de X (Features):", X.shape)
print("Forma de y (Target):", y.shape)
```

---

### Explicación y Complementos

Para que un modelo de regresión funcione, los datos no pueden entrar de cualquier forma. Aquí te explico el "porqué" de cada paso:

#### 1. Del DataFrame al Array (`.values`)

Aunque Pandas es excelente para manipular datos, scikit-learn prefiere trabajar con **arreglos de NumPy**. Al usar `.values`, eliminamos el índice y los encabezados de Pandas, dejando solo los valores numéricos puros que el algoritmo puede procesar matemáticamente.

#### 2. La Dimensión de $X$ vs. $y$

Esta es la regla de oro en scikit-learn:

- **$y$ (Variable Objetivo):** Puede ser una lista simple de valores (1D). Es solo el resultado que queremos adivinar.
    
- **$X$ (Características):** **SIEMPRE** debe ser una matriz (2D). Incluso si solo usas una columna (como "radio"), el modelo espera una estructura de "tabla" con filas y columnas.
    

#### 3. El truco de `.reshape(-1, 1)`

Cuando extraes una sola columna, NumPy te da un array plano (ej. `[10, 20, 30]`). Para convertirlo en una columna vertical (ej. `[[10], [20], [30]]`), usamos `reshape`:

- **El `-1`**: Es un comodín. Le dice a Python: _"No sé cuántas filas hay exactamente, calcúlalo tú basándote en el total de datos"_.
    
- **El `1`**: Dice: _"Obligatoriamente pon toda la información en una sola columna"_.
    

#### 4. Verificación con `.shape`

Al imprimir la forma, deberías ver algo como:

- `X.shape` -> `(n_muestras, 1)`: Indica que tienes $n$ filas y **1 columna**.
    
- `y.shape` -> `(n_muestras,)`: Indica que es una lista plana de $n$ elementos.
    

Si estas dimensiones coinciden en el número de muestras, tu conjunto de datos está listo para entrar al método `.fit()`.

---

## Construcción y Entrenamiento de un Modelo de Regresión Lineal


Con las matrices $X$ (característica "radio") y $y$ (objetivo "sales") preparadas, el objetivo es entrenar un modelo de **Regresión Lineal**. En este ejercicio, utilizaremos el conjunto de datos completo para modelar la relación histórica entre la inversión y las ventas, buscando la "línea de mejor ajuste".

```python
# 1. Importar LinearRegression
from sklearn.linear_model import LinearRegression

# 2. Instanciar el modelo
reg = LinearRegression()

# 3. Ajustar (entrenar) el modelo a los datos
# Aquí el modelo calcula la relación matemática entre radio y ventas
reg.fit(X, y)

# 4. Realizar predicciones
# Aplicamos el modelo entrenado sobre X para obtener las ventas estimadas
predictions = reg.predict(X)

# Verificamos las primeras cinco predicciones
print(predictions[:5])
```

---

### Explicación y Conceptos Clave

El proceso de entrenamiento en regresión lineal es uno de los conceptos más potentes y fundamentales del Machine Learning.

#### 1. El Proceso de Ajuste (`.fit`)

Cuando ejecutas `reg.fit(X, y)`, el algoritmo busca la **línea recta** que minimice la distancia entre ella y todos los puntos de datos reales. Matemáticamente, el modelo está calculando dos valores:

- **La Pendiente (a):** Qué tanto impacta cada dólar invertido en radio en las ventas finales.
    
- **La Intersección (b):** El valor estimado de ventas si la inversión en radio fuera cero.
    

#### 2. ¿Por qué no usamos Train/Test Split aquí?

Como menciona el ejercicio, a veces el objetivo no es predecir el futuro, sino **describir la relación actual**. Al usar todos los datos, obtenemos la descripción más precisa de cómo la publicidad ha afectado las ventas históricamente en este conjunto de datos específico.

#### 3. Generando Predicciones (`.predict`)

Una vez que el modelo tiene su "línea" definida, usamos `.predict(X)` para ver qué valores de ventas asignaría el modelo a cada nivel de inversión en radio que ya conocemos.

- **Dato técnico:** Si graficáramos estas `predictions`, obtendríamos una línea recta perfecta. Si graficamos `y` (los valores reales), veríamos puntos dispersos.
    

#### 4. Interpretación de los Resultados

Al ejecutar `print(predictions[:5])`, obtendrás una lista de números continuos. Estos representan los dólares que el modelo "cree" que se debieron ganar basándose en la tendencia general. Comparar estos números con las ventas reales es el primer paso para saber si nuestra publicidad en radio es un buen predictor.

## Visualizar un modelo de regresión lineal

Tras construir y entrenar el modelo de regresión lineal con todas las observaciones disponibles, el siguiente paso es la visualización. Esto permite interpretar visualmente qué tan bien se ajusta el modelo a los datos reales y entender la relación entre el gasto en publicidad de radio y los valores de ventas (_sales_). Para ello, utilizaremos un gráfico de dispersión para los datos reales y un gráfico de líneas para las predicciones.

```python
# Importar matplotlib.pyplot
import matplotlib.pyplot as plt

# Crear un gráfico de dispersión (scatter plot)
# Visualizamos los valores reales (y) frente a la característica (X)
plt.scatter(X, y, color="blue")

# Crear un gráfico de líneas (line plot)
# Dibujamos la línea de tendencia usando las predicciones del modelo
plt.plot(X, predictions, color="red")

# Añadir etiquetas a los ejes para mayor claridad
plt.xlabel("Radio Expenditure ($)")
plt.ylabel("Sales ($)")

# Visualizar el gráfico final
plt.show()
```

---

### Explicación

La visualización es una herramienta fundamental en la regresión para validar la calidad del modelo de forma intuitiva:

- **`plt.scatter(X, y, color="blue")`**: Esta función dibuja cada observación real como un punto en el plano. El eje horizontal ($X$) representa la inversión en radio y el eje vertical ($y$) las ventas obtenidas. Al usar el color azul para los datos reales, podemos observar la dispersión y la tendencia natural de los datos.
    
- **`plt.plot(X, predictions, color="red")`**: A diferencia del scatter plot, esta función conecta los puntos con una línea. Al pasarle las `predictions`, estamos dibujando la **Línea de Mejor Ajuste** (Line of Best Fit). Esta línea representa la "decisión" del modelo: es la trayectoria que minimiza la distancia total a todos los puntos azules.
    
- **Interpretación del gráfico**:
    
    - Si los puntos azules están muy cerca de la línea roja, significa que hay una **correlación fuerte** y el modelo es muy preciso.
        
    - La pendiente de la línea roja nos indica cuánto aumentan las ventas por cada dólar adicional invertido en radio.
        
    - Este gráfico confirma visualmente si la relación es efectivamente lineal o si un modelo de regresión lineal es adecuado para este problema específico.