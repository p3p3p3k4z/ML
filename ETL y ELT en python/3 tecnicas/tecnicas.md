# Apuntes de ETL y ELT en Python: Datos no Tabulares, Transformaciones Avanzadas y Carga a SQL

## 1. Introducción a los Datos no Tabulares

No todos los datos vienen en formato de tabla (filas y columnas). Fuentes como APIs, archivos JSON, logs, imágenes o texto enriquecido producen datos **no tabulares** o **semiestructurados**. Para integrarlos en un pipeline ETL, es necesario extraerlos y transformarlos a un formato tabular (como un DataFrame de pandas) que pueda ser procesado y analizado.

**Ejemplos comunes de datos no tabulares:**
- JSON anidado proveniente de APIs REST.
- Archivos de log con estructura variable.
- Documentos XML.
- Respuestas de servicios web.

El desafío principal es **aplanar** (flatten) estos datos, extrayendo la información relevante y organizándola en columnas.

---

## 2. Extracción de Datos JSON

### 2.1. ¿Qué es JSON?

JSON (JavaScript Object Notation) es un formato ligero de intercambio de datos, basado en pares **clave-valor**. Es el formato más común para APIs web.

**Características:**
- No tiene un esquema fijo (puede variar entre registros).
- Soporta anidamiento (objetos dentro de objetos).
- Su estructura se asemeja a los diccionarios de Python.

```json
{
  "timestamp": 863703000,
  "price": {
    "open": 0.121875,
    "close": 0.097917
  },
  "volume": 1443120000
}
```

### 2.2. Lectura de archivos JSON con el módulo `json`

Python incluye el módulo `json` para trabajar con este formato.

```python
import json

with open("raw_stock_data.json", "r") as file:
    raw_stock_data = json.load(file)

print(type(raw_stock_data))  # <class 'dict'>
```

- **`json.load()`** lee un archivo JSON y lo convierte en un diccionario de Python.
- Si el archivo contiene una lista de objetos, se obtendrá una lista de diccionarios.

### 2.3. Lectura directa con `pandas.read_json()`

pandas también puede leer JSON y convertirlo directamente a DataFrame, pero suele funcionar mejor con JSON planos (no anidados).

```python
import pandas as pd

df = pd.read_json("raw_stock_data.json")
```

Sin embargo, para JSON altamente anidados, es preferible usar `json.load()` y luego transformar manualmente.

---

## 3. Transformación de JSON Anidado a DataFrame

### 3.1. El problema del anidamiento

Los datos JSON suelen tener estructuras como esta:

```json
{
  "863703000": {
    "price": {
      "open": 0.121875,
      "close": 0.097917
    },
    "volume": 1443120000
  },
  "863789400": {
    "price": {
      "open": 0.098146,
      "close": 0.086458
    },
    "volume": 294000000
  }
}
```

Las claves externas (`863703000`, `863789400`) son los timestamps, y los valores internos contienen la información. Este formato no es directamente cargable en un DataFrame.

### 3.2. Iteración sobre diccionarios

Para aplanar, necesitamos recorrer el diccionario y extraer los valores deseados. Python ofrece varios métodos útiles:

```python
# Iterar solo sobre las claves
for key in raw_data.keys():
    ...

# Iterar solo sobre los valores
for value in raw_data.values():
    ...

# Iterar sobre pares clave-valor
for key, value in raw_data.items():
    ...
```

### 3.3. Extracción segura con `.get()`

Al trabajar con datos anidados, es recomendable usar el método `.get()` en lugar de acceder directamente con corchetes (`[]`). `.get()` permite:
- Evitar errores `KeyError` si una clave no existe.
- Proporcionar un valor por defecto.

```python
entry = {
    "volume": 1443120000,
    "price": {
        "open": 0.121875,
        "close": 0.097917
    }
}

# Acceso seguro a primer nivel
volume = entry.get("volume")  # 1443120000

# Valor por defecto si la clave no existe
ticker = entry.get("ticker", "DCMP")  # "DCMP"

# Acceso a objetos anidados
open_price = entry.get("price").get("open")  # 0.121875
# Alternativa más segura
open_price = entry.get("price", {}).get("open", 0)  # 0.121875
```

### 3.4. Construcción de una lista de filas

El proceso típico para transformar JSON anidado en DataFrame es:
1. Crear una lista vacía (`parsed_data = []`).
2. Iterar sobre los elementos del diccionario.
3. Para cada elemento, extraer los campos deseados y añadirlos como una lista (una fila) a `parsed_data`.
4. Convertir la lista de listas en DataFrame.

```python
parsed_stock_data = []

for timestamp, ticker_info in raw_stock_data.items():
    parsed_stock_data.append([
        timestamp,                                   # clave externa
        ticker_info.get("price", {}).get("open", 0), # open
        ticker_info.get("price", {}).get("close", 0),# close
        ticker_info.get("volume", 0)                  # volume
    ])

# Crear DataFrame
transformed_df = pd.DataFrame(parsed_stock_data)

# Asignar nombres de columnas
transformed_df.columns = ["timestamps", "open", "close", "volume"]

# Establecer columna como índice (opcional)
transformed_df = transformed_df.set_index("timestamps")
```

**Resultado:** un DataFrame limpio y listo para análisis o carga.

---

## 4. Transformaciones Avanzadas con pandas

Una vez que los datos están en formato tabular, pandas ofrece potentes herramientas para limpiar, enriquecer y agregar información.

### 4.1. Manejo de valores faltantes (`.fillna()`)

Los datos reales suelen tener valores nulos (NaN). `fillna()` permite reemplazarlos de diversas formas.

**Rellenar con un valor constante:**

```python
# Rellenar todos los NaN con 0
clean_df = raw_df.fillna(value=0)
```

**Rellenar con valores distintos por columna:**

```python
clean_df = raw_df.fillna(value={"open": 0, "close": 0.5})
```

**Rellenar usando otra columna:**

```python
# Rellenar valores faltantes de "open" con los de "close"
raw_df["open"].fillna(raw_df["close"], inplace=True)
```

### 4.2. Agrupación de datos (`.groupby()`)

El método `.groupby()` permite agregar datos según una o más columnas, similar a `GROUP BY` en SQL.

**Ejemplo:** Calcular el promedio de volumen, precio de apertura y cierre por cada ticker.

```python
grouped = raw_df.groupby(by=["ticker"], axis=0).mean()
```

**Otros agregados:** `.min()`, `.max()`, `.sum()`, `.count()`, etc.

### 4.3. Aplicación de funciones personalizadas (`.apply()`)

Cuando la funcionalidad necesaria no está disponible en métodos incorporados, se puede usar `.apply()` para aplicar una función a cada fila o columna.

**Ejemplo:** Clasificar cada registro como "Increase" o "Decrease" según la diferencia entre cierre y apertura.

```python
def classify_change(row):
    change = row["close"] - row["open"]
    return "Increase" if change > 0 else "Decrease"

# Aplicar la función a cada fila (axis=1)
raw_df["change"] = raw_df.apply(classify_change, axis=1)
```

**Antes:**

| ticker | open     | close    |
|--------|----------|----------|
| AAPL   | 0.121875 | 0.097917 |
| AAPL   | 0.098146 | 0.086458 |
| AMZN   | 0.247511 | 0.251290 |

**Después:**

| ticker | open     | close    | change   |
|--------|----------|----------|----------|
| AAPL   | 0.121875 | 0.097917 | Decrease |
| AAPL   | 0.098146 | 0.086458 | Decrease |
| AMZN   | 0.247511 | 0.251290 | Increase |

---

## 5. Carga de Datos a una Base de Datos SQL

Una vez transformados, los datos deben persistirse para su consumo. pandas facilita la carga a bases de datos SQL mediante el método `.to_sql()`.

### 5.1. Configuración de la conexión

Se necesita una **URI de conexión** y un **engine** de SQLAlchemy.

```python
import sqlalchemy

connection_uri = "postgresql+psycopg2://repl:password@localhost:5432/market"
db_engine = sqlalchemy.create_engine(connection_uri)
```

### 5.2. Uso de `.to_sql()`

```python
clean_stock_data.to_sql(
    name="filtered_stock_data",   # Nombre de la tabla
    con=db_engine,                 # Conexión
    if_exists="append",            # Comportamiento si la tabla existe: 'fail', 'replace', 'append'
    index=True,                     # ¿Incluir el índice del DataFrame como columna?
    index_label="timestamps"        # Nombre de la columna para el índice
)
```

**Parámetros importantes:**
- **`if_exists`**:
  - `'fail'`: lanza error si la tabla existe.
  - `'replace'`: borra y recrea la tabla.
  - `'append'`: añade filas a la tabla existente.
- **`index`**: si es `True`, el índice del DataFrame se guarda como una columna.
- **`index_label`**: nombre de esa columna.

### 5.3. Validación de la carga

Siempre es recomendable verificar que los datos se hayan persistido correctamente.

```python
# Leer los datos recién escritos
to_validate = pd.read_sql("SELECT * FROM filtered_stock_data", db_engine)

# Comparar número de filas
assert len(to_validate) == len(clean_stock_data)

# Comparar contenido (puede requerir ajustes por tipos)
# ...
```

---

## 6. Resumen y Buenas Prácticas

| Etapa | Herramientas clave | Buenas prácticas |
| :--- | :--- | :--- |
| **Extracción de no tabulares** | `json.load()`, `pd.read_json()` | Usar `.get()` para acceso seguro; manejar datos anidados con iteración. |
| **Transformación a tabular** | Iteración sobre dict, listas, `pd.DataFrame()` | Construir filas como listas, asignar nombres de columna, establecer índice. |
| **Limpieza y enriquecimiento** | `.fillna()`, `.groupby()`, `.apply()` | Documentar estrategias de imputación; validar resultados con `.head()`, `.info()`. |
| **Carga a SQL** | `.to_sql()`, SQLAlchemy | Elegir `if_exists` adecuado; validar la persistencia leyendo de vuelta. |

**Consideraciones adicionales:**
- Los datos JSON pueden ser muy grandes. Considerar lectura por partes (streaming) o uso de librerías como `ijson` para archivos enormes.
- Al aplanar JSON, decidir qué campos anidados mantener y cómo nombrar las columnas (ej. `price_open`, `price_close`).
- En entornos productivos, añadir logging y manejo de excepciones (como se vio en el capítulo anterior) para monitorizar el proceso.

Con estas técnicas, estarás preparado para incorporar fuentes de datos no tabulares en tus pipelines ETL, transformarlos eficientemente y cargarlos en bases de datos para su posterior análisis.