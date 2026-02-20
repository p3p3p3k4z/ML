Ejemplo de compañia de telecomunicaciones
Imagina que tenemos este pequeño DataFrame de Pandas llamado `df_ventas`:

|**total_day_charge**|**total_eve_charge**|**churn**|
|---|---|---|
|45.5|20.1|0|
|20.2|15.3|1|
|35.8|22.4|0|

---

### 1. Extrayendo $X$ (La Tabla de Atributos)

Para que scikit-learn no se queje, necesitamos que $X$ sea un objeto de **dos dimensiones**. En Pandas, si seleccionas las columnas usando una **lista de nombres** (con doble corchete `[[ ]]`), automáticamente te mantiene el formato de tabla (2D).


```python
# Usamos doble corchete para asegurar que sea 2D (Filas y Columnas)
X = df_ventas[['total_day_charge', 'total_eve_charge']].values

print(X.shape) 
# Resultado: (3, 2) -> 3 filas, 2 columnas. ¡Perfecto para sklearn!
```

---

### 2. Extrayendo $y$ (El Vector Objetivo)

Para la respuesta, solo queremos una lista simple de resultados. Al usar un solo corchete `['column']`, Pandas nos devuelve una Serie (1D).


```python
# Usamos un solo corchete para que sea 1D (Una lista simple)
y = df_ventas['churn'].values

print(y.shape) 
# Resultado: (3,) -> 3 elementos en una sola línea. ¡Justo lo que pide y!
```

---

### 3. El flujo completo con KNN

Ahora que ya tienes tus "piezas de Lego" ($X$ y $y$) con la forma correcta, armamos el modelo:


```python
from sklearn.neighbors import KNeighborsClassifier

# 1. Creamos el "cerebro" del modelo con 3 vecinos
knn = KNeighborsClassifier(n_neighbors=3)

# 2. Entrenamos (Ajustamos). Aquí sklearn cruza la tabla X con las etiquetas y
knn.fit(X, y)

# 3. Imagina que llega un cliente nuevo con:
# total_day_charge = 40.0 y total_eve_charge = 18.0
X_nuevo = [[40.0, 18.0]] # <--- NOTA: ¡También debe ser 2D! (Lista de listas)

# 4. Le pedimos al modelo que adivine
prediccion = knn.predict(X_nuevo)

print(f"¿El cliente se irá? (1=Sí, 0=No): {prediccion}")
```

### 🧠 ¿Por qué el `X_nuevo` también lleva doble corchete?

Porque aunque solo le estés preguntando por **un** cliente, el modelo está programado para recibir "una lista de clientes". Al poner `[[...]]`, le estás diciendo: _"Aquí tienes mi lista, que solo tiene un invitado con estos dos datos"_.

---

### Resumen para tu estudio:

- **$X$** = `df[['col1', 'col2']].values` (Doble corchete = Tabla 2D).
    
- **$y$** = `df['objetivo'].values` (Un corchete = Lista 1D).
    
- **`.values`** = El "traductor" que convierte los datos de Pandas a arrays de NumPy para que scikit-learn los entienda.
    

### Ejercicio
Ajustar KNN: k vecinos más cercanos
En este ejercicio, construirás tu primer modelo de clasificación utilizando el conjunto de datos `churn_df`, que se ha precargado para el resto del capítulo.

El objetivo, `"churn"`, tiene que ser una sola columna con el mismo número de observaciones que los datos de la característica. Los datos de las características ya se han convertido en matrices `numpy`.

`"account_length"` y `"customer_service_calls"` se tratan como características porque la duración de la cuenta indica fidelidad del cliente, las llamadas frecuentes al servicio de atención al cliente pueden ser señal de insatisfacción y ambas pueden ser buenos predictores de la rotación.
```python
# Import KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier

y = churn_df["churn"].values
X = churn_df[["account_length", "customer_service_calls"]].values

# 1. Creamos el clasificador KNN con 6 vecinos
# El parámetro se llama n_neighbors
knn = KNeighborsClassifier(n_neighbors=6)

# 2. Ajustamos (entrenamos) el clasificador a los datos
# Usamos el método .fit() pasando X (características) e y (objetivo)
knn.fit(X, y)
```

Predecir KNN: k vecinos más cercanos

Ahora que has ajustado un clasificador KNN, puedes utilizarlo para predecir la etiqueta de nuevos puntos de datos. Para el entrenamiento se utilizaron todos los datos disponibles, pero, afortunadamente, hay nuevas observaciones disponibles. Se han precargado para ti como `X_new`.

Se ha precargado el modelo `knn`, que creaste y ajustaste a los datos en el último ejercicio. Utilizarás tu clasificador para predecir las etiquetas de un conjunto de nuevos puntos de datos:

```
X_new = np.array([[30.0, 17.5],

                  [107.0, 24.1],

                  [213.0, 10.9]])
```

```python

```