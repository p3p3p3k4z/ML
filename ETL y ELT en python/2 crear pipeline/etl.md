# Apuntes de ETL y ELT en Python: Extracción, Transformación, Persistencia y Monitorización

## 1. Extracción de Datos desde Fuentes Estructuradas

La primera etapa de cualquier pipeline de datos es la extracción. Los datos pueden provenir de múltiples orígenes, y Python (con pandas) ofrece herramientas para leer desde los más comunes.

### 1.1. Fuentes de datos típicas

En este curso nos centraremos en:
- Archivos **CSV**
- Archivos **Parquet**
- Archivos **JSON**
- Bases de datos **SQL**

En el mundo real, los datos también se extraen de:
- APIs (REST, GraphQL)
- Data Lakes (almacenamiento en la nube)
- Data Warehouses (Snowflake, BigQuery, Redshift)
- Web scraping
- Y muchas más...

### 1.2. Lectura de archivos Parquet

**Parquet** es un formato de archivo de código abierto, orientado a columnas, diseñado para un almacenamiento y recuperación eficientes. Es muy utilizado en entornos de Big Data por su alto rendimiento y compresión.

```python
import pandas as pd

# Leer un archivo Parquet
raw_stock_data = pd.read_parquet("raw_stock_data.parquet", engine="fastparquet")
```

- **`engine`**: Puede ser `'fastparquet'` o `'pyarrow'`. Ambos son motores de lectura/escritura para Parquet.
- Al igual que con CSV, el resultado es un DataFrame de pandas.

### 1.3. Conexión a bases de datos SQL

Para extraer datos desde una base de datos SQL, necesitamos:
1. Una **URI de conexión** que especifique cómo conectarse.
2. Un **motor (engine)** de SQLAlchemy.
3. Una consulta SQL.

```python
import sqlalchemy
import pandas as pd

# URI de conexión: dialecto+driver://usuario:contraseña@host:puerto/base_de_datos
connection_uri = "postgresql+psycopg2://repl:password@localhost:5432/market"
db_engine = sqlalchemy.create_engine(connection_uri)

# Ejecutar consulta y cargar resultado en DataFrame
raw_stock_data = pd.read_sql("SELECT * FROM raw_stock_data LIMIT 10", db_engine)
```

- **`read_sql()`**: Ejecuta la consulta y devuelve un DataFrame.
- La URI varía según el motor de base de datos (PostgreSQL, MySQL, SQLite, etc.).

### 1.4. Modularidad: crear funciones reutilizables

Para construir pipelines mantenibles y legibles, es fundamental separar la lógica en funciones. Esto sigue el principio **DRY (Don't Repeat Yourself)** y facilita la depuración.

```python
def extract_from_sql(connection_uri, query):
    """Conecta a una base de datos SQL, ejecuta una consulta y devuelve un DataFrame."""
    db_engine = sqlalchemy.create_engine(connection_uri)
    return pd.read_sql(query, db_engine)

# Uso
datos = extract_from_sql(
    "postgresql+psycopg2://repl:password@localhost:5432/market",
    "SELECT * FROM raw_stock_data LIMIT 10;"
)
```

---

## 2. Transformación de Datos con pandas

La transformación es el corazón del pipeline. Aquí es donde los datos se limpian, filtran, enriquecen y preparan para su uso posterior.

### 2.1. Filtrado y selección con `.loc[]`

El método `.loc[]` permite acceder a un grupo de filas y columnas por etiquetas o mediante un array booleano.

```python
# Filtrar filas donde 'open' sea mayor que 0
cleaned = raw_stock_data.loc[raw_stock_data["open"] > 0, :]

# Seleccionar solo algunas columnas
cleaned = raw_stock_data.loc[:, ["timestamps", "open", "close"]]

# Combinar ambos en un solo paso
cleaned = raw_stock_data.loc[raw_stock_data["open"] > 0, ["timestamps", "open", "close"]]
```

### 2.2. Filtrado posicional con `.iloc[]`

`.iloc[]` funciona con índices enteros (posición), no con etiquetas. Es útil cuando se conoce la posición exacta de filas y columnas.

```python
# Seleccionar las primeras 50 filas y las columnas 0, 1 y 2
cleaned = raw_stock_data.iloc[0:50, [0, 1, 2]]
```

### 2.3. Conversión de tipos de fecha con `pd.to_datetime()`

Los formatos de fecha y hora suelen venir en representaciones no estándar. `pd.to_datetime()` es la herramienta para convertirlas a tipo `datetime` de pandas.

```python
# Caso 1: Formato de cadena "20230101085731" (YYYYMMDDHHMMSS)
cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], format="%Y%m%d%H%M%S")
# Resultado: Timestamp('2023-01-01 08:57:31')

# Caso 2: Timestamp en milisegundos (epoch)
cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], unit="ms")
# Resultado: Timestamp('2023-04-15 22:00:00.011000')
```

- **`format`**: Especifica el formato de la cadena de entrada.
- **`unit`**: Para valores numéricos, indica la unidad ('s', 'ms', 'us', 'ns').

### 2.4. Validación de transformaciones

Transformar datos conlleva riesgos: pérdida de información o creación de datos erróneos. Siempre hay que validar.

```python
# Ver las primeras filas
print(cleaned.head())

# Ver los registros más pequeños y más grandes según una columna
print(cleaned.nsmallest(10, ["timestamps"]))
print(cleaned.nlargest(10, ["timestamps"]))
```

- **`nsmallest()`** y **`nlargest()`**: Devuelven las n filas con los valores más pequeños o más grandes de la(s) columna(s) especificada(s).

---

## 3. Persistencia de Datos con pandas

Una vez transformados, los datos deben ser almacenados para que los consumidores (analistas, modelos, dashboards) puedan acceder a ellos.

### 3.1. Por qué persistir datos

- Garantiza un acceso estable a los datos transformados.
- Ocurre como paso final del proceso ETL, pero también puede ocurrir entre etapas (por ejemplo, guardar datos intermedios).
- Captura una "foto fija" (snapshot) de los datos en un momento dado.

### 3.2. Guardar a CSV con `.to_csv()`

```python
# Asumiendo que ya tenemos un DataFrame 'stock_data'
stock_data.to_csv("stock_data.csv")
```

### 3.3. Personalización del archivo CSV

```python
# Incluir o no el encabezado (header)
stock_data.to_csv("stock_data.csv", header=True)  # Por defecto True

# Cambiar el separador (por ejemplo, tubería |)
stock_data.to_csv("stock_data.csv", sep="|")

# Incluir o no el índice
stock_data.to_csv("stock_data.csv", index=False)  # Recomendado para evitar columnas extra
```

### 3.4. Otros formatos de salida

pandas ofrece métodos análogos para otros formatos:
- **`.to_parquet()`**: Para guardar en formato Parquet (eficiente para grandes volúmenes).
- **`.to_json()`**: Para JSON.
- **`.to_sql()`**: Para cargar directamente a una tabla SQL.

### 3.5. Verificar la persistencia

Siempre es buena práctica comprobar que el archivo se ha creado correctamente.

```python
import os

# ... (extracción, transformación, carga) ...

# Verificar que el archivo existe
if os.path.exists("stock_data.csv"):
    print("Archivo guardado correctamente.")
else:
    print("Error: el archivo no se creó.")
```

---

## 4. Monitorización de un Pipeline de Datos

Un pipeline en producción debe ser monitorizado para detectar problemas como datos faltantes, cambios en los tipos de datos, o fallos en la ejecución.

### 4.1. Logging con el módulo `logging`

El módulo `logging` de Python permite documentar el rendimiento y los eventos del pipeline.

```python
import logging

# Configuración básica
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

# Diferentes niveles de log
logging.debug(f"Variable tiene el valor {path}")
logging.info("Los datos han sido transformados y serán cargados.")
```

- **DEBUG**: Información detallada, normalmente solo para diagnóstico.
- **INFO**: Confirmación de que las cosas funcionan como se espera.
- **WARNING**: Indica que algo inesperado ocurrió, pero el pipeline puede continuar.
- **ERROR**: Problema grave que impide continuar con una parte del pipeline.

### 4.2. Logging de advertencias y errores

```python
logging.warning("Número inesperado de filas detectado.")
logging.error("Se produjo un error de tipo KeyError.")
```

### 4.3. Manejo de excepciones con `try-except`

El bloque `try-except` permite capturar errores y ejecutar lógica alternativa o de recuperación.

```python
try:
    # Código que puede fallar
    clean_stock_data = transform(raw_stock_data)
    logging.info("DataFrame filtrado correctamente por 'price_change'")
except KeyError as ke:
    # Manejar el error específico
    logging.warning(f"{ke}: No se puede filtrar por 'price_change'. Creando columna...")
    raw_stock_data["price_change"] = raw_stock_data["close"] - raw_stock_data["open"]
    clean_stock_data = transform(raw_stock_data)
```

- Capturar la excepción específica (como `KeyError`) en lugar de una genérica (`except:`) permite un manejo más preciso.
- Se puede registrar el error y luego tomar una acción correctiva (como crear la columna faltante).

---

## 5. Resumen y Buenas Prácticas

| Etapa | Herramientas clave | Buenas prácticas |
| :--- | :--- | :--- |
| **Extracción** | `pd.read_csv()`, `pd.read_parquet()`, `pd.read_sql()`, SQLAlchemy | Modularizar en funciones, usar URIs seguras, limitar filas en desarrollo. |
| **Transformación** | `.loc[]`, `.iloc[]`, `pd.to_datetime()`, `.nsmallest()`, `.nlargest()` | Validar cada paso, documentar transformaciones complejas, manejar valores nulos. |
| **Carga (Persistencia)** | `.to_csv()`, `.to_parquet()`, `.to_json()`, `.to_sql()` | Verificar la existencia del archivo, elegir formato según el caso de uso, no guardar el índice. |
| **Monitorización** | `logging`, `try-except`, `os.path.exists()` | Loguear eventos clave, capturar excepciones específicas, alertar sobre anomalías. |

Un pipeline bien construido es modular, está bien documentado mediante logs, maneja errores con gracia y persiste los datos de forma verificable. Esto garantiza que los datos lleguen a los consumidores finales de manera confiable y consistente.