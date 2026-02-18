## Machine Learning con scikit-learn

Este curso se centra en el aprendizaje supervisado utilizando **scikit-learn**, una de las bibliotecas más importantes y utilizadas en el ecosistema de Python para ciencia de datos.

### ¿Qué es el Machine Learning?

Es el proceso mediante el cual las computadoras aprenden a **tomar decisiones a partir de datos** sin necesidad de ser programadas explícitamente para cada tarea.

* **Ejemplo de Clasificación:** Predecir si un correo es spam o no spam basándose en su contenido y remitente.
* **Ejemplo de Agrupamiento:** Organizar libros en diferentes categorías según las palabras que contienen.

---

### Aprendizaje No Supervisado vs. Supervisado

Existen dos enfoques principales dependiendo de la naturaleza de los datos:

**Aprendizaje No Supervisado**
Es el proceso de descubrir **patrones y estructuras ocultas** en datos que **no tienen etiquetas** (unlabeled data).

* **Clustering (Agrupamiento):** Una empresa que desea agrupar a sus clientes en categorías basadas en su comportamiento de compra, sin conocer de antemano cuáles son esas categorías.

**Aprendizaje Supervisado**
Es un tipo de Machine Learning donde los valores que queremos predecir **ya son conocidos** en los datos de entrenamiento. El objetivo es construir un modelo que pueda predecir con precisión los valores de datos nuevos que nunca ha visto.

* Utiliza **Atributos (Features)** para predecir el valor de una **Variable Objetivo (Target variable)**.
* *Ejemplo:* Predecir la posición de un jugador de baloncesto basándose en sus puntos por partido.

---

### Tipos de Aprendizaje Supervisado

Dependiendo de lo que se desee predecir, el aprendizaje supervisado se divide en:

**Clasificación**
Se utiliza para predecir una **etiqueta o categoría** de una observación.

* **Clasificación Binaria:** Cuando solo hay dos resultados posibles (ej. una transacción bancaria es fraudulenta o no lo es).

**Regresión**
Se utiliza para predecir **valores continuos**.

* *Ejemplo:* Predecir el precio de una propiedad basándose en el número de habitaciones y el tamaño del terreno.

---

### Convenciones de Denominación

En el mundo del ML y la estadística, es común encontrar diferentes nombres para los mismos conceptos. En este curso y en la documentación de scikit-learn se usarán estas convenciones:

| Concepto | Otros nombres comunes | Símbolo usual |
| --- | --- | --- |
| **Atributo (Feature)** | Variable predictora / Variable independiente |  |
| **Variable Objetivo (Target)** | Variable dependiente / Respuesta |  |

---

### Requisitos Previos y EDA

Antes de aplicar cualquier modelo de aprendizaje supervisado, los datos deben cumplir con ciertos requisitos técnicos:

1. **Sin valores faltantes:** No debe haber huecos en la información.
2. **Formato numérico:** Los datos deben ser números (no texto).
3. **Estructura:** Deben estar almacenados como **DataFrames** o **Series** de pandas, o como **arrays de NumPy**.

Para asegurar esto, es fundamental realizar primero un **Análisis Exploratorio de Datos (EDA)** utilizando métodos de estadística descriptiva y visualizaciones de datos en pandas.

---

### Flujo de Trabajo y Sintaxis de scikit-learn

Una de las grandes ventajas de scikit-learn es que sigue la misma sintaxis para casi todos los modelos, lo que hace que el flujo de trabajo sea repetible.

El proceso estándar consta de cuatro pasos:

1. **Importar:** Traer el modelo (algoritmo) desde un módulo de `sklearn`.
* *Ejemplo:* El modelo **k-Nearest Neighbors (k-NN)**, que usa la distancia entre observaciones para predecir.


2. **Instanciar:** Crear una variable (generalmente llamada `model`) para inicializar el algoritmo.
3. **Entrenar (Fit):** El modelo aprende los patrones de los datos. Se le pasan los atributos () y la variable objetivo ().
4. **Predecir (Predict):** Se utiliza el método `.predict()` pasando nuevas observaciones () para obtener los resultados.

**Ejemplo de código conceptual:**

```python
# 1. Importar el modelo
from sklearn.neighbors import KNeighborsClassifier

# 2. Instanciar
model = KNeighborsClassifier(n_neighbors=6)

# 3. Entrenar el modelo con los datos
model.fit(X, y)

# 4. Predecir con datos nuevos
predictions = model.predict(X_new)

```

En el caso de un detector de spam, el método `predict` devolvería un array de ceros y unos:

* `1`: El modelo predice que es **Spam**.
* `0`: El modelo predice que **No es Spam**.
