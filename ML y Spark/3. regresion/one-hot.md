## One-Hot Encoding: Variables Categóricas a Numéricas 🔢

Muchos algoritmos de ML (como la regresión logística o lineal) **requieren que todas las variables de entrada sean numéricas**, ya que realizan cálculos matemáticos (sumas, multiplicaciones) sobre ellas.

Aquí surge un problema: ¿cómo representamos variables categóricas como "Color" (Rojo, Azul, Verde) o "Tipo de Auto" (Compacto, Deportivo, SUV) para que el modelo las entienda sin asumir un orden incorrecto?

-----

### El Problema de la Indexación Simple

Si simplemente asignamos un número a cada categoría (ej. Rojo=1, Azul=2, Verde=3), el modelo podría malinterpretar que Verde (3) es "mayor" o "mejor" que Rojo (1), o que el promedio de Rojo y Verde es Azul. ¡Esto no tiene sentido matemático para categorías sin orden natural\!

### La Solución: One-Hot Encoding 🔥

One-Hot Encoding resuelve esto creando **nuevas columnas binarias (ficticias o *dummy variables*)** para cada categoría posible.

  * **¿Cómo funciona?**

      * Crea una columna para cada valor único de la categoría.
      * En cada fila, coloca un **1** en la columna que corresponde a su categoría activa y **0** en todas las demás.
      * Es como un interruptor: solo una ("one") columna está encendida ("hot") a la vez.

  * **Ejemplo:**
    Si la columna original es "Color":
    | Color | -\> | Es\_Rojo | Es\_Azul | Es\_Verde |
    |---|---|---|---|---|
    | Rojo | -\> | 1 | 0 | 0 |
    | Verde | -\> | 0 | 0 | 1 |
    | Azul | -\> | 0 | 1 | 0 |

-----

### Representación Dispersa (Sparse Vectors) en Spark

Cuando tienes muchas categorías (ej. miles de códigos postales), crear miles de columnas llenas de ceros es muy ineficiente en memoria.

  * **Vectores Densos (Dense):** Almacenan todos los valores, incluyendo los ceros. Ej: `[1.0, 0.0, 0.0, 0.0, 7.0]`
  * **Vectores Dispersos (Sparse):** Solo almacenan los valores **distintos de cero** y sus posiciones (índices). Esto ahorra muchísimo espacio.
      * Formato: `(tamaño_total, [índices_activos], [valores_activos])`
      * Ej: `(5, [0, 4], [1.0, 7.0])` significa "un vector de tamaño 5, donde en la posición 0 hay un 1.0 y en la posición 4 hay un 7.0; todo lo demás es cero".

Spark usa automáticamente vectores dispersos para el resultado de `OneHotEncoder` para ser eficiente.

-----

### Implementación en Spark ML

En Spark, el proceso usualmente tiene dos pasos:

1.  **StringIndexer:** Convierte las categorías de texto a índices numéricos (0, 1, 2...).
2.  **OneHotEncoder:** Toma esos índices y los convierte en vectores binarios (dispersos).

<!-- end list -->

```python
from pyspark.ml.feature import StringIndexer, OneHotEncoder

# 1. Suponemos que ya aplicaste StringIndexer y tienes 'type_idx'

# 2. Crear el codificador One-Hot
# inputCols: columna(s) con índices numéricos.
# outputCols: nombre(s) de la(s) nueva(s) columna(s) de vectores dispersos.
onehot = OneHotEncoder(inputCols=['type_idx'], outputCols=['type_dummy'])

# Ajustar (fit) y transformar los datos
onehot_model = onehot.fit(cars)
cars = onehot_model.transform(cars)

# Resultado: 'type_dummy' contiene SparseVectors
cars.select('type', 'type_idx', 'type_dummy').show(truncate=False)
```

**Nota sobre "Redundant Column":** A veces, para evitar problemas matemáticos (colinealidad), se elimina una de las columnas ficticias (ej. si no es Rojo ni Azul, *tiene* que ser Verde, así que la columna "Es\_Verde" es redundante). Spark maneja esto con el parámetro `dropLast` (por defecto `True`), que elimina la última categoría para hacer los vectores más compactos y matemáticamente estables.