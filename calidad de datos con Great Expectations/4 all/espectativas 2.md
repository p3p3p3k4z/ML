# Apuntes de Great Expectations: Expectativas de Columna y Condicionales

## 1. Expectativas Básicas de Columna

Las expectativas de columna se dividen en dos categorías principales: **a nivel de fila** y **a nivel de agregado**. Las primeras verifican propiedades de cada valor individual, mientras que las segundas examinan estadísticas de toda la columna.

### 1.1. Expectativas a nivel de fila (Row-level)

Estas expectativas se aplican a cada valor de una columna y comprueban si cumplen una condición.

- **`ExpectColumnValuesToNotBeNull(column)`**: Verifica que no haya valores nulos en la columna.
- **`ExpectColumnValuesToBeOfType(column, type_)`**: Verifica que los valores de la columna sean de un tipo de datos específico (por ejemplo, `"str"`, `"int"`, `"float"`).

```python
import great_expectations as gx

# Expectativa de no nulos
expectation_null = gx.expectations.ExpectColumnValuesToNotBeNull(column="colour")

# Expectativa de tipo de datos
expectation_type = gx.expectations.ExpectColumnValuesToBeOfType(column="review_count", type_="str")
```

### 1.2. Expectativas a nivel de agregado (Aggregate-level)

Estas expectativas resumen la columna completa.

- **`ExpectColumnDistinctValuesToEqualSet(column, value_set)`**: El conjunto de valores distintos debe coincidir exactamente con `value_set`.
- **`ExpectColumnUniqueValueCountToBeBetween(column, min_value, max_value)`**: El número de valores únicos debe estar en un rango.
- **`ExpectColumnValuesToBeUnique(column)`**: Todos los valores de la columna deben ser únicos (sin duplicados).
- **`ExpectColumnMostCommonValueToBeInSet(column, value_set)`**: El valor más frecuente (moda) debe pertenecer a `value_set`.

```python
# Conjunto de valores distintos esperado
expectation_distinct = gx.expectations.ExpectColumnDistinctValuesToEqualSet(
    column="seller_name",
    value_set={"Womens Shoes"}
)

# Rango de valores únicos
expectation_unique_count = gx.expectations.ExpectColumnUniqueValueCountToBeBetween(
    column="review_count",
    min_value=5,
    max_value=101
)

# Valores únicos (sin duplicados)
expectation_unique = gx.expectations.ExpectColumnValuesToBeUnique(column="sku_id")

# Moda en un conjunto
expectation_mode = gx.expectations.ExpectColumnMostCommonValueToBeInSet(
    column="colour",
    value_set={"Khaki", "Purple", "Grey"}
)
```

---

## 2. Expectativas Específicas por Tipo de Dato

### 2.1. Expectativas para columnas numéricas

**A nivel de agregado** (estadísticos):

- `ExpectColumnMeanToBeBetween(column, min_value, max_value)`
- `ExpectColumnMedianToBeBetween(column, min_value, max_value)`
- `ExpectColumnStdevToBeBetween(column, min_value, max_value)`
- `ExpectColumnSumToBeBetween(column, min_value, max_value)`

```python
expectation_mean = gx.expectations.ExpectColumnMeanToBeBetween(
    column="mark_price_usd",
    min_value=20,
    max_value=25
)

expectation_median = gx.expectations.ExpectColumnMedianToBeBetween(
    column="mark_price_usd",
    min_value=20,
    max_value=25
)

expectation_stdev = gx.expectations.ExpectColumnStdevToBeBetween(
    column="mark_price_usd",
    min_value=15,
    max_value=20
)

expectation_sum = gx.expectations.ExpectColumnSumToBeBetween(
    column="mark_price_usd",
    min_value=20000,
    max_value=21000
)
```

**A nivel de fila** (rangos y orden):

- `ExpectColumnValuesToBeBetween(column, min_value, max_value)`: Cada valor debe estar en el rango.
- `ExpectColumnValuesToBeIncreasing(column)`: Los valores deben ser estrictamente crecientes (útil para series temporales).
- `ExpectColumnValuesToBeDecreasing(column)`: Los valores deben ser estrictamente decrecientes.

```python
# Valores entre 0 y 5
expectation_range = gx.expectations.ExpectColumnValuesToBeBetween(
    column="star_rating",
    min_value=0,
    max_value=5
)

# Valores crecientes
expectation_increasing = gx.expectations.ExpectColumnValuesToBeIncreasing(column="price_usd")
```

### 2.2. Expectativas para columnas de texto (string)

**Longitud de cadenas**:

- `ExpectColumnValueLengthsToEqual(column, value)`: La longitud de cada valor debe ser exactamente `value`.

**Coincidencia con expresiones regulares**:

- `ExpectColumnValuesToMatchRegex(column, regex)`: Cada valor debe cumplir la expresión regular.
- `ExpectColumnValuesToMatchRegexList(column, regex_list)`: Cada valor debe cumplir al menos una de las expresiones de la lista.

**Parseabilidad**:

- `ExpectColumnValuesToBeDateutilParseable(column)`: Los valores deben ser parseables como fechas por `dateutil`.
- `ExpectColumnValuesToBeJsonParseable(column)`: Los valores deben ser parseables como JSON.

```python
# Longitud exacta
expectation_length = gx.expectations.ExpectColumnValueLengthsToEqual(column="sku_id", value=18)

# Regex individual
expectation_regex = gx.expectations.ExpectColumnValuesToMatchRegex(
    column="link",
    regex="^https://us.shein.com/[\\w-]+"
)

# Lista de regex (ejemplo para imágenes)
regex_list = [
    "/img.ltwebstatic.com/images3_(spmp)|(pi)/202[0-4]/[0-1][0-9]/.*",
    "/sheinsz.ltwebstatic.com/she_dist/images/bg-.*"
]
expectation_regex_list = gx.expectations.ExpectColumnValuesToMatchRegexList(
    column="hero_image",
    regex_list=regex_list
)

# Parseabilidad de fechas
expectation_date = gx.expectations.ExpectColumnValuesToBeDateutilParseable(column="colour")  # ¿tiene sentido? Depende del contexto

# Parseabilidad JSON
expectation_json = gx.expectations.ExpectColumnValuesToBeJsonParseable(column="colour")
```

---

## 3. Expectativas Condicionales

A veces no queremos aplicar una expectativa a todas las filas, sino solo a un subconjunto que cumple cierta condición. Para ello se usan los parámetros `row_condition` y `condition_parser`.

### 3.1. Sintaxis

- **`row_condition`**: Expresión booleana (como cadena) que define el subconjunto de datos al que aplicar la expectativa.
- **`condition_parser`**: Debe ser `"pandas"` cuando se trabaja con DataFrames de pandas. Define la sintaxis de `row_condition`.

### 3.2. Reglas para escribir `row_condition`

- No usar comillas simples dentro de la expresión (pueden causar errores de parseo). Es mejor usar comillas dobles o escapar adecuadamente.
- No usar saltos de línea.
- La sintaxis es similar a la de pandas, pero sin el prefijo `df.` (se asume que la columna es un nombre de variable). Por ejemplo:

| Expresión pandas | `row_condition` equivalente |
| :--- | :--- |
| `df["foo"] == 'Two Two'` | `'foo == "Two Two"'` |
| `df["foo"].notnull()` | `'foo.notnull()'` |
| `df["foo"] <= datetime.date(2023,3,13)` | `'foo <= datetime.date(2023,3,13)'` (requiere importar datetime en el contexto de validación) |
| `(df["foo"] > 5) & (df["foo"] <= 3.14)` | `'(foo > 5) & (foo <= 3.14)'` |
| `df["foo"].str.startswith("bar")` | `'foo.str.startswith("bar")'` |

### 3.3. Ejemplo práctico

Supongamos que queremos validar que el precio (`price_usd`) sea menor o igual a 10, pero solo cuando el precio de marca (`mark_price_usd`) sea menor que 10.

```python
expectation = gx.expectations.ExpectColumnValuesToBeBetween(
    column="price_usd",
    max_value=10,
    condition_parser="pandas",
    row_condition='mark_price_usd < 10'
)

validation_results = batch.validate(expect=expectation)
print(validation_results.success)
```

**Nota**: La condición se aplica **antes** de evaluar la expectativa; solo las filas que cumplen la condición son evaluadas.

---

## 4. Resumen General del Curso (Wrap-Up)

### 4.1. Capítulo 1: Conexión a los datos

```python
# Crear Data Context
context = gx.get_context()

# Añadir Data Source (pandas)
data_source = context.data_sources.add_pandas(name="mi_fuente")

# Añadir Data Asset
data_asset = data_source.add_dataframe_asset(name="mi_asset")

# Definir Batch (todo el DataFrame)
batch_definition = data_asset.add_batch_definition_whole_dataframe(name="mi_batch_def")

# Obtener Batch con datos reales
batch = batch_definition.get_batch(batch_parameters={"dataframe": df})
```

### 4.2. Capítulo 2: Creación de Expectativas y Suites

```python
# Crear expectativa individual
expectation = gx.expectations.ExpectTableRowCountToEqual(value=118000)

# Validar contra batch
validation_results = batch.validate(expect=expectation)

# Crear Suite
suite = gx.ExpectationSuite(name="mi_suite")
suite.add_expectation(expectation)

# Validar Suite
validation_results = batch.validate(expect=suite)

# Añadir Suite al contexto
suite = context.suites.add(suite)

# Crear Validation Definition
validation_definition = gx.ValidationDefinition(
    name="mi_validacion",
    data=batch_definition,
    suite=suite
)

# Ejecutar Validation Definition
validation_results = validation_definition.run(batch_parameters={"dataframe": df})
```

### 4.3. Capítulo 3: Uso en la práctica (Checkpoints y gestión de componentes)

```python
# Añadir Validation Definition al contexto
validation_definition = context.validation_definitions.add(validation_definition)

# Crear Checkpoint
checkpoint = gx.Checkpoint(
    name="mi_checkpoint",
    validation_definitions=[validation_definition]
)

# Ejecutar Checkpoint
checkpoint_results = checkpoint.run(batch_parameters={"dataframe": df})
print(checkpoint_results.success)

# Copiar expectativa entre Suites
copia = expectation.copy()
copia.id = None
otra_suite.add_expectation(expectation=copia)

# Modificar y guardar
expectation.value = nuevo_valor
expectation.save()
suite.save()

# Eliminar expectativa
suite.delete_expectation(expectation)

# Gestionar componentes
context.suites.add(suite)
context.suites.get(name="mi_suite")
context.suites.all()
context.suites.delete(name="mi_suite")
```

### 4.4. Capítulo 4: Expectativas de columna (este capítulo)

Se han cubierto expectativas a nivel de fila y agregado, específicas para tipos numéricos y de cadena, y condicionales.

---

## 5. Recursos adicionales

- **Documentación oficial de Great Expectations Core**: [https://docs.greatexpectations.io/docs/core/introduction](https://docs.greatexpectations.io/docs/core/introduction)
- **Referencia de expectativas**: [https://docs.greatexpectations.io/docs/reference](https://docs.greatexpectations.io/docs/reference)
- **Galería de expectativas**: [www.greatexpectations.io/expectations](http://www.greatexpectations.io/expectations)

---

## 6. Cheat Sheet Consolidado del Capítulo 4

| Tipo | Expectativa | Descripción |
| :--- | :--- | :--- |
| **Row-level** | `ExpectColumnValuesToNotBeNull(column)` | Sin nulos |
| | `ExpectColumnValuesToBeOfType(column, type_)` | Tipo de datos |
| **Aggregate** | `ExpectColumnDistinctValuesToEqualSet(column, set)` | Conjunto de valores distintos |
| | `ExpectColumnUniqueValueCountToBeBetween(column, min, max)` | Número de únicos en rango |
| | `ExpectColumnValuesToBeUnique(column)` | Todos los valores únicos |
| | `ExpectColumnMostCommonValueToBeInSet(column, set)` | Moda dentro de un conjunto |
| **Numeric (agg)** | `ExpectColumnMeanToBeBetween(column, min, max)` | Media |
| | `ExpectColumnMedianToBeBetween(column, min, max)` | Mediana |
| | `ExpectColumnStdevToBeBetween(column, min, max)` | Desviación estándar |
| | `ExpectColumnSumToBeBetween(column, min, max)` | Suma |
| **Numeric (row)** | `ExpectColumnValuesToBeBetween(column, min, max)` | Valores en rango |
| | `ExpectColumnValuesToBeIncreasing(column)` | Estrictamente creciente |
| | `ExpectColumnValuesToBeDecreasing(column)` | Estrictamente decreciente |
| **String** | `ExpectColumnValueLengthsToEqual(column, value)` | Longitud exacta |
| | `ExpectColumnValuesToMatchRegex(column, regex)` | Coincidencia con regex |
| | `ExpectColumnValuesToMatchRegexList(column, list)` | Coincidencia con alguna regex |
| | `ExpectColumnValuesToBeDateutilParseable(column)` | Parseable como fecha |
| | `ExpectColumnValuesToBeJsonParseable(column)` | Parseable como JSON |
| **Conditional** | Añadir `condition_parser='pandas'` y `row_condition` | Aplicar solo a subconjunto |
