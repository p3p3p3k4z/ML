# Apuntes de Introducción a la Calidad de Datos con Great Expectations

## 1. ¿Qué es la Calidad de Datos?

La **calidad de datos** se define como el grado en que un conjunto de datos es adecuado para su propósito previsto. Un dato de alta calidad es aquel que se puede utilizar de manera confiable para tomar decisiones, entrenar modelos o generar reportes.

### 1.1. Dimensiones de la calidad de datos

Existen múltiples dimensiones que determinan la calidad de un dataset:

| Dimensión | Descripción |
| :--- | :--- |
| **Completitud (Completeness)** | ¿Todos los datos esperados están presentes? (ej. sin valores nulos excesivos). |
| **Precisión (Accuracy)** | ¿Los datos representan correctamente la realidad? |
| **Validez (Validity)** | ¿Los datos cumplen con las reglas de formato y tipo definidas? |
| **Unicidad (Uniqueness)** | ¿Hay duplicados que no deberían existir? |
| **Oportunidad (Timeliness)** | ¿Los datos están actualizados y disponibles cuando se necesitan? |
| **Integridad (Integrity)** | ¿Se mantienen las relaciones y reglas definidas entre datos? |
| **Consistencia (Consistency)** | ¿Los datos son coherentes entre sí a través del tiempo y diferentes fuentes? |

### 1.2. Importancia de la calidad de datos

> **Un modelo solo puede ser tan bueno como los datos que lo alimentan.**

La calidad de los datos impacta directamente en:
- **Modelos de Machine Learning:** Datos incorrectos o sucios producen modelos sesgados o poco precisos.
- **Toma de decisiones:** Decisiones basadas en datos erróneos pueden tener consecuencias costosas.
- **Eficiencia operativa:** Limpiar datos en producción es más costoso que prevenir problemas en etapas tempranas.

---

## 2. Introducción a Great Expectations

**Great Expectations (GX)** es una plataforma de código abierto diseñada para gestionar y mejorar la calidad de los datos a lo largo del ciclo de vida de los pipelines.

### 2.1. Modos de uso

Great Expectations ofrece dos formas principales de interactuar con la plataforma:

- **GX Cloud:** Versión con interfaz web (UI) que facilita la gestión centralizada.
- **GX Core:** Biblioteca de Python que permite trabajar programáticamente con todas las funcionalidades.

En este curso nos centramos en **GX Core**, que se instala como un paquete Python.

### 2.2. Concepto fundamental: Expectation (Expectativa)

Una **Expectation** es una afirmación verificable sobre los datos. Es el núcleo de Great Expectations. Las expectativas son aserciones que puedes definir para validar si tus datos cumplen ciertas condiciones.

**Ejemplos de expectativas:**
- El dataset debe tener un número específico de filas.
- No debe haber valores nulos en una columna crítica.
- Los valores de una columna deben ser únicos.
- Una columna debe contener valores dentro de un rango específico (ej. temperatura entre -50 y 50).
- El formato de una columna de fechas debe ser `YYYY-MM-DD`.
- La distribución de los datos debe ser similar a la de un conjunto de referencia.

Las expectativas son la base para **validar**, **documentar** y **monitorear** la calidad de los datos.

---

## 3. Configuración Inicial: Crear un Data Context

El **Data Context** es el punto de entrada principal en Great Expectations. Es un objeto que gestiona la configuración, los almacenes (stores) y el estado de tu proyecto GX.

### 3.1. Importar Great Expectations

```python
import great_expectations as gx
```

Se usa comúnmente el alias `gx` por convención.

### 3.2. Crear el Data Context

La función `get_context()` crea (si no existe) o carga el Data Context actual.

```python
context = gx.get_context()
print(context)
```

**Salida típica (resumida):**

```
{
  "analytics_enabled": true,
  "config_version": 4.0,
  "data_context_id": "5b407294-b17c-43e3-aa5f-4f8a4741e772",
  "expectations_store_name": "default_expectations_store",
  "validation_results_store_name": "default_validations_store",
  ...
}
```

Este objeto `context` será el que utilices para todas las operaciones posteriores: conectar a datos, crear expectativas, ejecutar validaciones, etc.

---

## 4. Conectar a los Datos

Para que Great Expectations pueda validar tus datos, primero debe saber cómo acceder a ellos. Esto se hace a través de dos conceptos: **Data Source** y **Data Asset**.

### 4.1. Data Source (Fuente de Datos)

Un **Data Source** es un objeto que le dice a GX cómo conectarse a una fuente de datos externa específica. Puede ser un archivo CSV, una base de datos, un DataFrame de pandas, etc.

En este capítulo trabajamos con la fuente **pandas**, que permite conectar GX a DataFrames.

```python
data_source = context.data_sources.add_pandas(
    name="my_pandas_datasource"
)
```

- El parámetro `name` es el nombre interno que GX usará para identificar esta fuente. Puede ser diferente del nombre de la variable Python (`data_source`).

### 4.2. Data Asset (Activo de Datos)

Una vez que tienes un Data Source, defines **Data Assets** dentro de él. Un Data Asset representa un conjunto de datos específico dentro de esa fuente (por ejemplo, una tabla, un archivo, o en este caso, un DataFrame).

```python
data_asset = data_source.add_dataframe_asset(
    name="my_dataframe_asset"
)
```

### 4.3. Cheat sheet: Creación de Data Source y Data Asset

```python
# Crear Data Source pandas
data_source = context.data_sources.add_pandas(name="nombre_fuente")

# Crear Data Asset (para DataFrames)
data_asset = data_source.add_dataframe_asset(name="nombre_asset")
```

---

## 5. Leer Datos en Batches

GX trabaja con el concepto de **Batch** (lote). Un Batch es un grupo de registros sobre el cual se pueden ejecutar validaciones.

### 5.1. Batch Definition (Definición de Lote)

Primero, se define un **Batch Definition** a partir del Data Asset. Esto especifica qué tipo de datos se van a tomar (por ejemplo, todo el DataFrame).

```python
batch_definition = data_asset.add_batch_definition_whole_dataframe(
    name="my_batch_definition"
)
```

- **`add_batch_definition_whole_dataframe`**: indica que el batch será el DataFrame completo.

### 5.2. Obtener un Batch

Finalmente, se obtiene un **Batch** concreto pasando los parámetros necesarios (en este caso, el DataFrame real).

```python
batch = batch_definition.get_batch(
    batch_parameters={"dataframe": dataframe}
)
```

Donde `dataframe` es tu DataFrame de pandas existente.

### 5.3. Explorar el Batch object

El objeto `batch` tiene métodos similares a los de pandas para inspeccionar los datos.

- **`batch.head()`** : Muestra las primeras filas (por defecto 5). Calcula las métricas necesarias.

```python
print(batch.head())
```

Salida (con barra de progreso):
```
Calculating Metrics: 100%|...| 1/1 [00:00<00:00, ...]
   Location           Date_Time  Temperature_C  Humidity_pct  Precipitation_mm  Wind_Speed_kwh
0  Chicago 2024-01-06 02:59:46      26.786811     31.513614          0.496024       22.980095
1  Chicago 2024-04-16 00:07:29      17.587820     32.817923          0.128803        0.234146
...
```

- **`batch.head(fetch_all=True)`** : Muestra todas las filas.

```python
print(batch.head(fetch_all=True))
```

- **`batch.columns()`** : Devuelve la lista de nombres de columnas (¡notar los paréntesis!).

```python
print(batch.columns())
# ['Location', 'Date_Time', 'Temperature_C', 'Humidity_pct', 'Precipitation_mm', 'Wind_Speed_kwh']
```

### 5.4. Cheat sheet: Creación de Batch

```python
# Crear Batch Definition
batch_definition = data_asset.add_batch_definition_whole_dataframe(
    name="nombre_definicion"
)

# Obtener Batch con un DataFrame específico
batch = batch_definition.get_batch(
    batch_parameters={"dataframe": mi_dataframe}
)

# Inspeccionar
print(batch.head())
print(batch.columns())
```

---

## 6. Resumen: Flujo de trabajo inicial en GX

```mermaid
graph LR
    A[Data Context] --> B[Data Source (pandas)]
    B --> C[Data Asset (dataframe)]
    C --> D[Batch Definition (whole dataframe)]
    D --> E[Batch]
    E --> F[Validaciones]
```

**Pasos resumidos:**
1. Crear o cargar el **Data Context**.
2. Añadir un **Data Source** (pandas, SQL, etc.).
3. Añadir un **Data Asset** (representa un DataFrame o tabla).
4. Definir un **Batch Definition** (cómo se tomarán los datos).
5. Obtener un **Batch** con los datos reales.
6. (Próximos capítulos) Definir Expectativas y validar el Batch.

| Concepto | Propósito | Ejemplo de código |
| :--- | :--- | :--- |
| **Data Context** | Punto de entrada y configuración global | `context = gx.get_context()` |
| **Data Source** | Define cómo conectar a una fuente externa | `context.data_sources.add_pandas(name="...")` |
| **Data Asset** | Representa un conjunto de datos específico | `data_source.add_dataframe_asset(name="...")` |
| **Batch Definition** | Define qué datos componen un lote | `data_asset.add_batch_definition_whole_dataframe(...)` |
| **Batch** | Lote concreto de datos para validar | `batch_definition.get_batch(batch_parameters={...})` |
