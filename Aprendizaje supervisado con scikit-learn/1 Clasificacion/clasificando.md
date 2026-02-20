## El Reto de la Clasificación: Algoritmo KNN

La clasificación es el proceso de construir un modelo (clasificador) que aprende de datos etiquetados para predecir la etiqueta de datos nuevos (no vistos).

### ¿Qué es k-Nearest Neighbors (KNN)?

La idea central de KNN es simple: **"Dime con quién andas y te diré quién eres"**. Para predecir la etiqueta de un punto de datos desconocido, el algoritmo mira a los $k$ puntos etiquetados más cercanos y toma una decisión.

- **Votación por Mayoría:** El modelo cuenta las etiquetas de esos $k$ vecinos y asigna al punto nuevo la etiqueta que tenga la mayoría.
    

> 💡 **Analogía del vecindario:** Imagina que te mudas a una casa pero no sabes si el barrio es "Ruidoso" o "Tranquilo". Preguntas a tus 3 vecinos más cercanos ($k=3$). Si dos dicen "Ruidoso" y uno dice "Tranquilo", tú clasificas tu casa como "Ruidosa" por votación de mayoría.

### El Impacto de "k"

El valor de $k$ es un **hiperparámetro** (un ajuste que tú eliges) y puede cambiar totalmente el resultado:

- **Si $k=3$:** Se miran los 3 vecinos más cercanos. Si 2 son rojos y 1 es azul, el nuevo punto será **Rojo**.
    
- **Si $k=5$:** Se amplía el círculo. Si ahora hay 3 azules y 2 rojos, el mismo punto será clasificado como **Azul**.
    

### Intuición y Frontera de Decisión

Cuando un modelo KNN termina de "aprender", divide el espacio de los datos en regiones. A esto se le llama **Frontera de Decisión (Decision Boundary)**.

- **Área de Predicción:** Es como un mapa político. Si un nuevo dato cae en la "zona gris", el modelo predice automáticamente una etiqueta (ej. el cliente se irá de la empresa / _churn_). Si cae en la "zona roja", predice otra (ej. el cliente se queda).
    

---

### Implementación Técnica con scikit-learn

Para usar KNN en código, debemos seguir reglas específicas sobre cómo estructurar la información.

#### La forma de los datos (Shapes)

Scikit-learn es muy estricto con las dimensiones de tus matrices:

- **Variable $X$ (Atributos):** Debe ser un array de **2 dimensiones**. Imaginalo como una tabla de Excel donde cada columna es una característica (ej. precio, tamaño) y cada fila es una observación.
    
- **Variable $y$ (Objetivo):** Debe ser un array de **1 dimensión**. Es una sola columna con las etiquetas (ej. 0 o 1).
    

> 🛠️ **Nota técnica:** Usamos el atributo `.values` de pandas para convertir nuestras tablas en **arrays de NumPy**, que es el formato de bajo nivel que scikit-learn procesa más rápido.

#### El proceso en código

Python

```
from sklearn.neighbors import KNeighborsClassifier

# 1. Instanciar el modelo (Elegimos k=15)
knn = KNeighborsClassifier(n_neighbors=15)

# 2. Ajustar (Fit) el modelo
# Aquí el modelo "se sitúa" en el mapa de los datos etiquetados
knn.fit(X, y)

# 3. Predecir (Predict)
# Pasamos datos nuevos (X_new) para ver qué etiquetas les asigna
predictions = knn.predict(X_new)
```

Al imprimir las predicciones, obtendrás valores binarios (como `1` para "se va" o `0` para "se queda") por cada observación que hayas pasado en `X_new`.

---

### $X$: La Matriz de Atributos (2D)

La $X$ siempre es una **matriz**. En términos de programación, es una "lista de listas" o un array de dos dimensiones.

- **Las Filas:** Representan a cada **sujeto u observación** (en nuestro ejemplo, cada invitado).
    
- **Las Columnas:** Representan las **características o atributos** (features) que estamos midiendo de ese sujeto.
    

Aunque solo tengas **un solo atributo** (por ejemplo, cuántas cervezas tomó cada invitado), scikit-learn sigue esperando una estructura de tabla (2D).

> 💡 **La analogía del expediente:** Imagina que tienes un archivero. Cada carpeta es una fila (un invitado). Dentro de la carpeta hay varias hojas, cada una con un dato (edad, hambre, humor). Eso es 2D: **Filas (personas) x Columnas (datos).**

---

### $y$: El Vector Objetivo (1D)

La $y$ es un **vector**. Es una sola columna, una lista simple.

- **¿Por qué es 1D?** Porque para cada observación (cada fila de $X$), solo queremos predecir **una sola cosa**. En nuestro ejemplo: ¿Se divirtió? (Sí/No).
    
- No necesitas columnas extra, porque $y$ es simplemente la "etiqueta" o la respuesta final vinculada a cada fila de $X$.
    

---

### ¿Cómo se ve esto en código?

Si intentas pasarle a scikit-learn una lista simple para $X$, te lanzará un error porque espera "forma de tabla". Mira la diferencia:

Python

```
# Esto es 1D (Forma de 'y')
# Una lista simple de resultados
y = [1, 0, 1] 

# Esto es 2D (Forma de 'X')
# Aunque solo sea un dato por persona, nota los corchetes dobles [[ ]]
# Es una tabla de 3 filas y 1 columna
X = [
    [10], # Invitado 1 tomó 10 cervezas
    [2],  # Invitado 2 tomó 2 cervezas
    [8]   # Invitado 3 tomó 8 cervezas
]
```

### ¿Por qué scikit-learn es tan "especial" con esto?

Porque los algoritmos están diseñados matemáticamente para realizar operaciones de **álgebra lineal**. Multiplican la matriz $X$ por un conjunto de pesos. Si $X$ no tiene forma de matriz (2D), la matemática "no encaja" y el programa truena.

---

**Resumen rápido para tus notas:**

- **$X$ (Features):** Siempre **2D** `[Filas, Columnas]`. Es la información que describe al objeto.
    
- **$y$ (Target):** Siempre **1D** `[Resultados]`. Es la respuesta que queremos predecir.
    
