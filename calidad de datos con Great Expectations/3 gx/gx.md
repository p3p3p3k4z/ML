# Apuntes de Great Expectations: Checkpoints, Actualización de Suites y Gestión de Componentes

## 1. Checkpoints: Automatización y Acciones

### 1.1. ¿Qué es un Checkpoint?

Un **Checkpoint** es un objeto de Great Expectations que agrupa una o más **Validation Definitions** y las ejecuta con parámetros compartidos. Su objetivo es automatizar la validación de datos y, opcionalmente, desencadenar **acciones** basadas en los resultados (por ejemplo, enviar notificaciones, generar documentación, etc.).

- **Validation Definition**: vincula una Expectation Suite con un Batch Definition.
- **Checkpoint**: ejecuta una o varias Validation Definitions sobre un mismo conjunto de datos (Batch) y puede ejecutar acciones post-validación.

### 1.2. Ventajas de usar Checkpoints

- **Reutilización**: un solo Checkpoint puede lanzar múltiples validaciones.
- **Acciones**: integración con herramientas externas (Slack, email, Data Docs, etc.) basada en el éxito/fallo de las validaciones.
- **Orquestación**: permite centralizar la lógica de validación en entornos de producción.

### 1.3. Creación de un Checkpoint

```python
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint
from great_expectations.checkpoint.actions import SlackNotificationAction

# Supongamos que ya tenemos una validation_definition creada
checkpoint = Checkpoint(
    name="mi_checkpoint",
    validation_definitions=[validation_definition],
    actions=[SlackNotificationAction()]  # opcional
)
```

**Importante**: Al igual que con otros componentes, el Checkpoint debe ser añadido al Data Context antes de ejecutarse.

### 1.4. Error común: Validation Definition no añadida al contexto

Si intentamos ejecutar el Checkpoint sin haber añadido previamente la Validation Definition al Data Context, obtendremos un error similar a:

```
CheckpointRelatedResourcesFreshnessError:
ValidationDefinition 'mi_validation_definition' must be added to the DataContext...
```

**Solución**: Añadir la Validation Definition al contexto antes de crear el Checkpoint, o al menos antes de ejecutarlo.

```python
validation_definition = context.validation_definitions.add(validation_definition)
```

### 1.5. Ejecución de un Checkpoint

Para ejecutar el Checkpoint, se utiliza el método `.run()` pasando los parámetros del batch (por ejemplo, el DataFrame a validar).

```python
checkpoint_results = checkpoint.run(
    batch_parameters={"dataframe": dataframe}
)
```

Los resultados incluyen información detallada de cada validación, el éxito global, y enlaces a GX Cloud si está configurado.

```python
print(checkpoint_results.success)        # Booleano global
print(checkpoint_results.describe())     # Resumen de validaciones
```

### 1.6. Acciones (Slack, Data Docs, etc.)

Las acciones se ejecutan automáticamente después de la validación. Por ejemplo, `SlackNotificationAction()` puede enviar un mensaje a un canal de Slack con un resumen. Great Expectations ofrece varias acciones predefinidas y permite crear personalizadas.

---

## 2. Actualización de Expectation Suites

### 2.1. Copiar expectativas entre Suites

Una Expectation no puede pertenecer a dos Suites simultáneamente. Si se intenta añadir la misma expectativa a otra Suite, se produce un error:

```
RuntimeError: Cannot add Expectation because it already belongs to an ExpectationSuite...
```

**Solución**: Copiar la expectativa y eliminar su identificador único (`.id`).

```python
expectation_copy = expectation.copy()
expectation_copy.id = None
otra_suite.add_expectation(expectation=expectation_copy)
```

### 2.2. Verificar si una Expectative pertenece a una Suite

```python
print(expectation in suite.expectations)   # True o False
```

### 2.3. Eliminar una Expectativa de una Suite

```python
suite.delete_expectation(expectation=expectation)
```

### 2.4. Modificar una Expectativa existente

Para cambiar el valor de una expectativa (por ejemplo, el número esperado de filas), se modifica el atributo correspondiente y se guarda.

```python
expectation.value = 11           # Cambiar valor
expectation.save()                # Guardar cambios
```

**Nota**: La expectativa debe pertenecer a una Suite; de lo contrario, `.save()` lanzará un error.

### 2.5. Guardar una Expectation Suite después de cambios

Después de añadir, modificar o eliminar expectativas, es necesario guardar la Suite para que los cambios persistan y estén disponibles para futuras validaciones.

```python
suite.save()
```

Si no se guarda y se intenta ejecutar una Validation Definition que usa esa Suite, se producirá un error de sincronización:

```
ResourceFreshnessAggregateError: ExpectationSuite 'my_suite' has changed since it has last been saved...
```

---

## 3. Gestión de Componentes en el Data Context

El Data Context (`context`) actúa como un repositorio central que almacena y gestiona todos los objetos de Great Expectations: Data Sources, Expectation Suites, Validation Definitions y Checkpoints.

Cada tipo de componente tiene su propio "almacén" accesible mediante atributos del contexto:

- `context.data_sources`
- `context.suites`
- `context.validation_definitions`
- `context.checkpoints`

### 3.1. Añadir componentes

```python
# Añadir una Expectation Suite
suite = context.suites.add(suite)

# Añadir una Validation Definition
validation_definition = context.validation_definitions.add(validation_definition)

# Añadir un Checkpoint
checkpoint = context.checkpoints.add(checkpoint)

# Añadir un Data Source (método específico para pandas)
data_source = context.data_sources.add_pandas(name="mi_fuente_pandas")
```

### 3.2. Recuperar componentes por nombre

```python
data_source = context.data_sources.get(name="mi_fuente_pandas")
suite = context.suites.get(name="mi_suite")
validation_definition = context.validation_definitions.get(name="mi_validacion")
checkpoint = context.checkpoints.get(name="mi_checkpoint")
```

### 3.3. Listar todos los componentes

```python
# Obtener todos los Data Sources
todos_data_sources = context.data_sources.all()

# Listar todas las Suites
todas_suites = context.suites.all()
```

El método `.all()` devuelve una estructura (normalmente un diccionario) con los nombres y metadatos de los componentes.

### 3.4. Eliminar componentes

```python
context.data_sources.delete(name="mi_fuente_pandas")
context.suites.delete(name="mi_suite")
context.validation_definitions.delete(name="mi_validacion")
context.checkpoints.delete(name="mi_checkpoint")
```

**Precaución**: La eliminación es permanente. Asegúrate de que el componente ya no es necesario.

---

## 4. Cheat Sheet Resumen

### Checkpoints

```python
# Crear Checkpoint (sin acciones)
checkpoint = gx.Checkpoint(
    name="mi_checkpoint",
    validation_definitions=[validation_definition]
)

# Añadir Validation Definition al contexto (obligatorio)
validation_definition = context.validation_definitions.add(validation_definition)

# Ejecutar Checkpoint
resultados = checkpoint.run(batch_parameters={"dataframe": df})
print(resultados.success)
print(resultados.describe())
```

### Copiar expectativas entre Suites

```python
copia = expectation.copy()
copia.id = None
otra_suite.add_expectation(expectation=copia)
```

### Modificar y guardar expectativas

```python
expectation.value = nuevo_valor
expectation.save()                # Guardar cambios en la expectativa
suite.save()                       # Guardar cambios en la suite (opcional tras save)
```

### Eliminar expectativa

```python
suite.delete_expectation(expectation=expectation)
```

### Gestión de componentes

| Operación | Data Sources | Suites | Validation Definitions | Checkpoints |
| :--- | :--- | :--- | :--- | :--- |
| **Añadir** | `context.data_sources.add_pandas(name)` | `context.suites.add(suite)` | `context.validation_definitions.add(vd)` | `context.checkpoints.add(cp)` |
| **Obtener por nombre** | `.get(name)` | `.get(name)` | `.get(name)` | `.get(name)` |
| **Listar todos** | `.all()` | `.all()` | `.all()` | `.all()` |
| **Eliminar** | `.delete(name)` | `.delete(name)` | `.delete(name)` | `.delete(name)` |

---

## 5. Flujo de trabajo típico con Checkpoints

1. **Preparar los datos**: tener un DataFrame y un Batch Definition.
2. **Crear Expectation Suite** con las validaciones deseadas.
3. **Crear Validation Definition** que vincule la Suite con el Batch Definition.
4. **Añadir la Validation Definition al contexto**.
5. **Crear Checkpoint** que use esa Validation Definition (y opcionalmente acciones).
6. **Añadir el Checkpoint al contexto** (si se desea persistir).
7. **Ejecutar el Checkpoint** con los datos actuales.
8. **Analizar resultados** y, si se configuraron acciones, recibir notificaciones.
