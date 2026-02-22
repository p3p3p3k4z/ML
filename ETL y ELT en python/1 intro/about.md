# Apuntes de ETL y ELT en Python: Introducción a Pipelines de Datos

## 1. ¿Qué son los Data Pipelines?

Los **pipelines de datos** (data pipelines) son sistemas que se encargan de mover datos desde un origen (source) hasta un destino (destination), aplicando transformaciones en el camino. Son fundamentales para procesos de **Business Intelligence (BI)**, **Machine Learning (ML)** e **Inteligencia Artificial (IA)**, ya que garantizan que los datos estén limpios, estructurados y listos para su análisis.

Un pipeline típico consta de tres etapas principales:
- **Extracción (Extract)**: Obtener datos de fuentes diversas (archivos, bases de datos, APIs, etc.).
- **Transformación (Transform)**: Limpiar, filtrar, agregar o enriquecer los datos.
- **Carga (Load)**: Almacenar los datos transformados en un destino (data warehouse, base de datos, archivo, etc.).

---

## 2. ETL vs. ELT: Dos Enfoques de Pipelines

### 2.1. ETL (Extract, Transform, Load)

Es el patrón tradicional. Los datos se extraen, se transforman en un entorno intermedio (generalmente con herramientas como Python y pandas) y luego se cargan en el destino.

**Ventajas**:
- Control total sobre la transformación.
- Ideal para fuentes no tabulares o cuando se requiere lógica compleja.
- Reduce la carga en el destino final.

**Ejemplo típico**:
```python
def extract(file_name):
    return pd.read_csv(file_name)

def transform(data_frame):
    # Limpieza, filtrado, etc.
    return data_frame.dropna()

def load(data_frame, target_table):
    data_frame.to_sql(name=target_table, con=POSTGRES_CONNECTION)

# Ejecución del pipeline
datos_crudos = extract("raw_data.csv")
datos_limpios = transform(datos_crudos)
load(datos_limpios, "cleaned_data")
```

### 2.2. ELT (Extract, Load, Transform)

Es un patrón más reciente, popularizado por los **data warehouses modernos** (Snowflake, BigQuery, Redshift). Los datos se extraen y se cargan directamente en el data warehouse (en bruto), y luego se transforman dentro del mismo usando SQL.

**Ventajas**:
- Aprovecha la potencia de procesamiento del data warehouse.
- Mayor escalabilidad para grandes volúmenes de datos.
- Simplifica el código de extracción.

**Ejemplo típico**:
```python
def extract(file_name):
    return pd.read_csv(file_name)

def load(data_frame, table_name):
    data_frame.to_sql(name=table_name, con=WAREHOUSE_CONNECTION)

def transform(source_table, target_table):
    data_warehouse.execute(f"""
        CREATE TABLE {target_table} AS
        SELECT column1, column2, ...
        FROM {source_table}
        WHERE condition;
    """)

# Ejecución del pipeline
datos_crudos = extract("raw_data.csv")
load(datos_crudos, "raw_data")
transform("raw_data", "cleaned_data")
```

---

## 3. Herramientas Principales en Python

### 3.1. Pandas para manipulación de datos

**Lectura de archivos CSV**:
```python
import pandas as pd

df = pd.read_csv("raw_data.csv", delimiter=",", header=0)
print(df.head())  # Muestra las primeras filas
```

- **`read_csv()`**: Lee un CSV y devuelve un DataFrame.
- Parámetros útiles: `delimiter`, `header`, `engine`, `encoding`.

**Filtrado de DataFrames** con `.loc`:
```python
# Filtrar filas donde la columna 'name' sea "Apparel"
df_filtrado = df.loc[df["name"] == "Apparel", :]

# Seleccionar solo las columnas 'name' y 'num_firms'
df_columnas = df.loc[:, ["name", "num_firms"]]

# Combinar ambos filtros
df_resultado = df.loc[df["name"] == "Apparel", ["name", "num_firms"]]
```

- `.loc` selecciona datos basados en etiquetas.
- El primer argumento es el filtro de filas, el segundo es el de columnas. `:` significa "todas".

**Escritura a archivos**:
```python
# Guardar DataFrame a CSV
df.to_csv("cleaned_data.csv", index=False)

# También se puede guardar a JSON, Excel, etc.
df.to_json("cleaned_data.json")
df.to_excel("cleaned_data.xlsx")
```

- `index=False` evita que se escriba el índice como columna.

### 3.2. Interacción con bases de datos SQL

**Conexión y ejecución de consultas**:
```python
# Suponiendo un cliente de base de datos (por ejemplo, psycopg2 para PostgreSQL)
cursor.execute("""
    CREATE TABLE total_sales AS
    SELECT ds, SUM(sales)
    FROM raw_sales_data
    GROUP BY ds;
""")
```

- Se pueden usar ORMs como SQLAlchemy o directamente cursores para ejecutar SQL.
- Para cargar DataFrames a SQL, pandas ofrece `to_sql()`.

---

## 4. Construcción de un Pipeline ETL Completo

Vamos a crear un pipeline que:
1. Extrae datos de un CSV.
2. Filtra las filas correspondientes a un sector específico (ej. "Apparel").
3. Guarda el resultado en un nuevo CSV.

```python
import pandas as pd

def extract(file_name):
    """Extrae datos desde un archivo CSV."""
    return pd.read_csv(file_name)

def transform(data_frame, sector):
    """Filtra el DataFrame por el sector deseado y selecciona columnas."""
    return data_frame.loc[data_frame["name"] == sector, ["name", "num_firms"]]

def load(data_frame, file_name):
    """Carga el DataFrame transformado a un archivo CSV."""
    data_frame.to_csv(file_name, index=False)

# Ejecución del pipeline
datos = extract("raw_data.csv")
datos_transformados = transform(datos, sector="Apparel")
load(datos_transformados, "cleaned_data.csv")
```

Este ejemplo muestra la estructura modular y reutilizable que deben tener los pipelines.

---

## 5. Buenas Prácticas y Consideraciones Adicionales

### 5.1. Pruebas Unitarias (Unit Testing)
- Verificar que cada función (extract, transform, load) se comporta como se espera.
- Ejemplo: probar que `transform()` devuelva un DataFrame vacío si el sector no existe.

### 5.2. Monitoreo (Monitoring)
- Registrar logs de cada etapa: cuántas filas se extrajeron, cuántas se transformaron, errores.
- Usar herramientas como `logging` en Python.

### 5.3. Despliegue a Producción (Deployment)
- Empaquetar el pipeline como un script ejecutable o como parte de un orquestador (Apache Airflow, Prefect).
- Asegurar la idempotencia: ejecutar el pipeline múltiples veces debe producir el mismo resultado.

### 5.4. Manejo de Datos Tabulares y No Tabulares
- **Tabulares**: CSV, Excel, tablas SQL. Se trabajan bien con pandas.
- **No tabulares**: JSON anidado, imágenes, logs. Pueden requerir transformaciones más complejas (por ejemplo, aplanar JSON).

---

## 6. Resumen

| Concepto | ETL | ELT |
| :--- | :--- | :--- |
| **Orden** | Extract → Transform → Load | Extract → Load → Transform |
| **Lugar de transformación** | Entorno intermedio (Python, Spark) | Dentro del data warehouse (SQL) |
| **Ideal para** | Datos complejos, fuentes no tabulares | Grandes volúmenes, data warehouses modernos |
| **Herramientas Python** | pandas, PySpark, dplyr | Clientes SQL, SQLAlchemy |

Los pipelines de datos son la columna vertebral de cualquier proyecto data-driven. Dominar ETL y ELT con Python te permitirá construir sistemas robustos y escalables para alimentar de datos confiables a tus modelos y dashboards.
