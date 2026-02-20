Los sistemas rara vez entregan la información "masticada". En el mundo real, los datos vienen sucios, incompletos y, sobre todo, en formatos no numéricos.

Aquí tienes el apunte formal sobre el preprocesamiento de datos categóricos, estructurado para tu colección profesional.

---

## Preprocesamiento: Manejo de Datos Categóricos

### 1. Definición y Requisitos de Scikit-learn

Para que cualquier modelo de **scikit-learn** funcione, los datos deben cumplir dos reglas de oro:

1. Deben ser puramente **numéricos**.
    
2. No deben contener **valores faltantes** (missing values).
    

Dado que gran parte de la información del mundo real es categórica (ej. géneros musicales, ciudades, colores), el preprocesamiento es el puente necesario para transformar estas categorías en una representación matemática que el algoritmo pueda entender.

---

### 2. Variables Ficticias (Dummy Variables)

La técnica estándar para convertir categorías en números es la creación de **variables ficticias** (también conocido como _One-Hot Encoding_).

**Características:**

- Se crea una nueva columna binaria (0 o 1) por cada categoría única.
    
- **La Regla del $N-1$:** Si una característica tiene 10 categorías (como géneros musicales), solo necesitamos 9 variables ficticias.
    
    - _¿Por qué?_ Si un registro tiene un "0" en las primeras 9 columnas, implícitamente pertenece a la décima. Mantener las 10 columnas crearía información redundante (multicolinealidad), lo que puede afectar negativamente a ciertos modelos de regresión.
        

---

### 3. Implementación con Pandas

Aunque scikit-learn tiene su propio `OneHotEncoder`, en el análisis exploratorio y prototipado rápido se prefiere `pandas.get_dummies()` por su simplicidad.


```python
import pandas as pd

# 1. Crear variables ficticias para la columna 'genre'
# drop_first=True elimina la primera columna para cumplir la regla N-1
music_dummies = pd.get_dummies(music_df["genre"], drop_first=True)

# 2. Concatenar con el DataFrame original y eliminar la columna categórica
music_df = pd.concat([music_df, music_dummies], axis=1)
music_df = music_df.drop("genre", axis=1)
```

#### Automática de todo el DataFrame

Si pasas todo el DataFrame a la función, Pandas identificará automáticamente las columnas de tipo `object` o `category` y las transformará, añadiendo un prefijo.


```python
# Proceso simplificado
music_dummies = pd.get_dummies(music_df, drop_first=True)

# Resultado: Las columnas se llamarán 'genre_Electronic', 'genre_Rock', etc.
print(music_dummies.columns)
```

---

### 4. Evaluación del Modelo con Datos Preprocesados

Al usar estas nuevas variables en una regresión, scikit-learn utiliza una métrica específica en la validación cruzada: `neg_mean_squared_error`.

**¿Por qué negativa?**

Scikit-learn tiene la filosofía de que "puntuaciones más altas son mejores". Como el Error Cuadrático Medio ($MSE$) es mejor cuando es **bajo**, scikit-learn le cambia el signo a negativo para que el valor "más alto" (más cercano a cero) sea el ganador.

$$RMSE = \sqrt{-(\text{neg\_mean\_squared\_error})}$$

```python
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression
import numpy as np

kf = KFold(n_splits=5, shuffle=True, random_state=42)
linreg = LinearRegression()

# Ejecutar CV usando el error cuadrático medio negativo
cv_results = cross_val_score(linreg, X, y, cv=kf, scoring="neg_mean_squared_error")

# Convertir a RMSE positivo para interpretación humana
rmse = np.sqrt(-cv_results)
print("Promedio RMSE: {}".format(np.mean(rmse)))
```

---

### Complemento para tu perfil (Ingeniería/DevOps)

El manejo de variables ficticias es crucial no solo para el modelo, sino para la **infraestructura de datos**. Al convertir una columna de texto en 10 columnas binarias, el tamaño de tu dataset crece. En entornos de **Big Data**, esto puede impactar la memoria del servidor. Siempre evalúa si todas las categorías son necesarias o si puedes agrupar las menos frecuentes en una categoría llamada "Otros".

