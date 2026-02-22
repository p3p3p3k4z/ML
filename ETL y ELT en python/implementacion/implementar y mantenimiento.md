# Apuntes de ETL y ELT en Python: Pruebas, Despliegue y Mantenimiento de Pipelines

## 1. La Importancia de Probar los Pipelines de Datos

Los pipelines de datos son componentes críticos en cualquier organización data-driven. Un fallo en el pipeline puede provocar decisiones erróneas, pérdidas económicas y daño reputacional. Por ello, **probar exhaustivamente** los pipelines es fundamental.

### 1.1. Beneficios de las pruebas

- **Validación del comportamiento:** Aseguran que los datos se extraen, transforman y cargan según lo esperado.
- **Reducción del esfuerzo de mantenimiento:** Detectar errores tempranamente evita costosas correcciones post-despliegue.
- **Mejora de la calidad y confiabilidad de los datos:** Identifican problemas de calidad antes de que afecten a los consumidores.
- **Documentación viva:** Las pruebas sirven como especificación del comportamiento esperado.

### 1.2. Tipos de pruebas en pipelines de datos

- **Pruebas end-to-end (integración):** Verifican que todo el pipeline funciona correctamente de principio a fin.
- **Validación en puntos de control (checkpoints):** Examinan los datos en etapas intermedias (tras extracción, tras transformación, etc.).
- **Pruebas unitarias:** Validan funciones individuales (como `extract()`, `transform()`, `load()`) de forma aislada.

---

## 2. Entornos de Prueba y Producción

Es crucial separar los entornos para evitar que las pruebas interfieran con los datos reales o con los consumidores.

- **Entorno de desarrollo:** Donde se construye y prueba inicialmente el pipeline.
- **Entorno de prueba (staging):** Réplica del entorno de producción, utilizado para pruebas integradas y de aceptación.
- **Entorno de producción:** Donde el pipeline opera con datos reales y sirve a los usuarios finales.

Las pruebas deben ejecutarse primero en entornos no productivos antes de promover el pipeline a producción.

---

## 3. Pruebas End-to-End y Validación de Checkpoints

### 3.1. Pruebas end-to-end

Consisten en ejecutar el pipeline completo con un conjunto de datos de prueba y verificar que el resultado final es el esperado. Esto incluye:

- Confirmar que el pipeline se ejecuta sin errores en múltiples intentos.
- Validar que los datos cargados en el destino coinciden con lo esperado.
- Realizar revisiones por pares (peer review) del código y los resultados.
- Asegurar que los consumidores (analistas, modelos, dashboards) pueden acceder y usar los datos correctamente.

### 3.2. Validación de checkpoints

Además de probar el resultado final, es útil inspeccionar los datos en puntos intermedios del pipeline. Por ejemplo, después de la extracción o después de la transformación.

```python
import pandas as pd
import sqlalchemy

# Configuración de conexión a la base de datos destino
connection_uri = "postgresql+psycopg2://repl:password@localhost:5432/market"
db_engine = sqlalchemy.create_engine(connection_uri)

# Cargar datos transformados (simulación)
clean_stock_data = pd.DataFrame(...)  # Resultado de la transformación

# Cargar a la base de datos
clean_stock_data.to_sql("clean_stock_data", db_engine, if_exists="replace")

# Validar checkpoint: leer los datos recién cargados
loaded_data = pd.read_sql("SELECT * FROM clean_stock_data", db_engine)

# Verificar dimensiones
print(loaded_data.shape)  # (6438, 4)

# Verificar primeras filas
print(loaded_data.head())

# Comparar DataFrames (contenido, no solo forma)
assert clean_stock_data.equals(loaded_data)
```

- **`equals()`** compara si dos DataFrames tienen el mismo contenido y tipo. Útil para validaciones exhaustivas.

---

## 4. Pruebas Unitarias con `pytest`

Las pruebas unitarias son una práctica estándar en ingeniería de software que se aplica también a pipelines de datos. Se centran en verificar funciones individuales.

### 4.1. Estructura básica de una prueba unitaria

Supongamos que tenemos un módulo `pipeline_utils.py` con funciones `extract`, `transform`, `load`. Creamos un archivo de pruebas (por ejemplo, `test_pipeline.py`).

```python
import pandas as pd
from pipeline_utils import extract, transform, load

def test_transformed_data():
    raw_data = extract("raw_stock_data.csv")
    clean_data = transform(raw_data)
    assert isinstance(clean_data, pd.DataFrame)
```

Para ejecutar las pruebas, usamos `pytest` en la terminal:

```bash
pytest test_pipeline.py
```

Salida esperada:
```
test_transformed_data . [100%]
1 passed in 1.17s
```

### 4.2. Uso de `assert` e `isinstance`

- **`assert condición`** : Lanza una excepción `AssertionError` si la condición es falsa. Si es verdadera, no hace nada.
- **`isinstance(objeto, tipo)`** : Verifica si un objeto es de un tipo determinado.

```python
pipeline_type = "ETL"

# Verificación simple
assert pipeline_type == "ETL"

# Verificación de tipo
assert isinstance(pipeline_type, str)

# Si falla, se lanza AssertionError
assert isinstance(pipeline_type, float)  # AssertionError
```

### 4.3. Fixtures en `pytest`

Los **fixtures** permiten crear datos o configuraciones reutilizables para múltiples pruebas. Por ejemplo, podemos tener un fixture que proporcione datos limpios.

```python
import pytest

@pytest.fixture
def clean_data():
    raw_data = extract("raw_stock_data.csv")
    clean = transform(raw_data)
    return clean

def test_transformed_data(clean_data):
    assert isinstance(clean_data, pd.DataFrame)
    assert len(clean_data.columns) == 4
    assert clean_data["open"].min() >= 0
    assert clean_data["open"].max() <= 1000
```

En esta prueba, `clean_data` se obtiene automáticamente del fixture, y luego se realizan múltiples aserciones:
- Número de columnas correcto.
- Valores dentro de rangos esperados.
- Se pueden encadenar condiciones con `and`.

---

## 5. Ejecución de un Pipeline en Producción

Una vez que el pipeline ha sido probado exhaustivamente, se puede desplegar en producción. Esto implica:

- Empaquetar el código (por ejemplo, en un script Python).
- Manejar errores y logging.
- Orquestar la ejecución (programada o bajo demanda).

### 5.1. Estructura modular

Es recomendable separar las funciones en módulos y luego crear un script principal que las importe y ejecute.

```
etl_pipeline.py
pipeline_utils.py
```

**pipeline_utils.py**:
```python
import pandas as pd

def extract(file_path):
    return pd.read_csv(file_path)

def transform(df):
    # Lógica de transformación...
    return df

def load(df):
    df.to_csv("cleaned_data.csv", index=False)
```

**etl_pipeline.py**:
```python
from pipeline_utils import extract, transform, load

raw_data = extract("raw_stock_data.csv")
clean_data = transform(raw_data)
load(clean_data)
```

### 5.2. Logging y manejo de excepciones

En producción, es esencial registrar lo que sucede y manejar fallos gracefulmente.

```python
import logging
from pipeline_utils import extract, transform, load

# Configurar logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

try:
    # Ejecutar pipeline
    raw_data = extract("raw_stock_data.csv")
    clean_data = transform(raw_data)
    load(clean_data)
    logging.info("Pipeline ejecutado exitosamente.")
except Exception as e:
    logging.error(f"El pipeline falló con el error: {e}")
    # Aquí se podría enviar una alerta (email, Slack, etc.)
```

- Se usa `try-except` para capturar cualquier excepción.
- Se registra con `logging.info` en caso de éxito y `logging.error` en caso de fallo.
- El nivel de log puede ajustarse (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

### 5.3. Orquestación de pipelines

En entornos reales, los pipelines rara vez se ejecutan manualmente. Se utilizan **orquestadores** como:

- **Apache Airflow**
- **Prefect**
- **Dagster**
- **Luigi**

Estas herramientas permiten:
- Programar ejecuciones (diarias, horarias, etc.).
- Gestionar dependencias entre tareas.
- Reintentar tareas fallidas.
- Proporcionar una interfaz de monitoreo.

---

## 6. Resumen del Curso y Próximos Pasos

### 6.1. Lo aprendido

- **Diseño de pipelines sólidos:** Estructura ETL/ELT, modularidad.
- **Extracción, transformación y carga:** Desde fuentes estructuradas (CSV, Parquet, SQL) y no estructuradas (JSON anidado).
- **Transformaciones avanzadas:** Manejo de nulos, agrupaciones, funciones personalizadas.
- **Persistencia:** Carga a archivos y bases de datos SQL.
- **Pruebas:** End-to-end, checkpoints, unit testing con `pytest`.
- **Manejo de errores y logging.**
- **Despliegue y orquestación.**

### 6.2. Habilidades adquiridas

- Capacidad para construir pipelines de datos confiables y mantenibles.
- Uso profesional de pandas para transformaciones.
- Aplicación de principios de ingeniería de software (pruebas, modularidad) al ámbito de datos.

### 6.3. Rutas de aprendizaje recomendadas

Para profundizar y especializarse, se sugiere:

- **Curso "Introduction to Airflow in Python"** (DataCamp) – Para dominar la orquestación.
- **Data Engineer Career Track** – Formación integral.
- **Certificación Associate Data Engineer** – Validación oficial.
- **Explorar herramientas como Apache Airflow, Astronomer, Snowflake** – Tecnologías clave en el ecosistema moderno.

---

## Conclusión

Un pipeline de datos bien diseñado no solo extrae, transforma y carga datos correctamente, sino que también es **fiable, mantenible y observable**. La combinación de pruebas automatizadas, logging adecuado y orquestación profesional garantiza que los datos lleguen a sus consumidores de forma consistente y con alta calidad. Este capítulo cierra el ciclo, preparándote para desplegar pipelines en entornos productivos con confianza.