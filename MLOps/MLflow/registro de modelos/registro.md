# MLflow Model Registry: Gestión Centralizada del Ciclo de Vida de Modelos

## 1. Introducción al Model Registry

El **Model Registry** es un componente de MLflow que actúa como un almacén centralizado y colaborativo para gestionar todo el ciclo de vida de los modelos de machine learning. Mientras que MLflow Tracking se enfoca en la experimentación (loguear parámetros, métricas y artefactos), el Model Registry se ocupa de la **gestión de modelos después del entrenamiento**, permitiendo versionarlos, etiquetarlos con etapas (stages) y facilitar su despliegue controlado.

### 1.1. Características Principales (según diapositiva 3)

- **Almacenamiento centralizado:** Un único lugar para todos los modelos importantes.
- **Gestión del ciclo de vida:** Control sobre cómo un modelo pasa de desarrollo a producción.
- **Web UI:** Interfaz gráfica para explorar y administrar modelos.
- **Cliente MLflow (`MlflowClient`):** API para interactuar programáticamente.
- **Versiones de modelo (Model Versions):** Cada modelo registrado puede tener múltiples versiones.
- **Etapas de modelo (Model Stages):** Etiquetas como `Staging`, `Production`, `Archived` para indicar el estado de una versión.

### 1.2. Modelo vs. Modelo Registrado (Diapositiva 4)

- **Modelo (Model):** Es el artefacto generado durante un entrenamiento y logueado en MLflow Tracking (por ejemplo, con `mlflow.sklearn.log_model()`). Inicialmente no está "registrado".
- **Modelo Registrado (Registered Model):** Es una entidad en el Model Registry que agrupa versiones de un mismo modelo (ej. "Unicorn"). Cuando registras un modelo, obtiene un número de versión y puede asignarse a una etapa.

---

## 2. Componentes del Model Registry

### 2.1. Versiones de Modelo (Model Versions) - Diapositiva 5

- Cada vez que registras un modelo bajo el mismo nombre, se incrementa automáticamente el número de versión (v1, v2, v3...).
- Esto permite rastrear cambios, mejoras y mantener un historial completo, similar al control de versiones en software.

### 2.2. Etapas de Modelo (Model Stages) - Diapositiva 5 y 29

Cada versión de un modelo puede estar en una de las siguientes etapas predefinidas:

- **None:** Estado por defecto al registrar un nuevo modelo. Aún no se ha asignado a ninguna etapa.
- **Staging:** Para modelos en fase de prueba o validación (pre-producción).
- **Production:** Modelo activo que está sirviendo predicciones en producción.
- **Archived:** Versiones antiguas o descartadas, que ya no se usan pero se conservan para trazabilidad.

**Regla:** Una versión solo puede tener una etapa a la vez (Diapositiva 29).

---

## 3. Trabajando con el Model Registry (Programáticamente)

### 3.1. El Cliente MLflow (`MlflowClient`)

Para interactuar con el Model Registry (y también con Tracking) de forma más avanzada, se utiliza la clase `MlflowClient`. (Diapositiva 8)

```python
from mlflow import MlflowClient

# Crear una instancia del cliente (apunta al tracking URI configurado)
client = MlflowClient()
```

### 3.2. Crear un Modelo Registrado (Diapositiva 9)

```python
# Crear un modelo registrado llamado "Unicorn"
client.create_registered_model(name="Unicorn")
```

Esto devuelve un objeto con metadatos como `creation_timestamp`, `name`, etc. Inicialmente no tiene versiones.

### 3.3. Buscar Modelos Registrados (Diapositivas 12-13)

Puedes buscar modelos usando filtros similares a SQL.

- **Identificadores:** `name`, `tags.<key>`.
- **Comparadores:** `=`, `!=`, `LIKE` (sensible a mayúsculas), `ILIKE` (insensible).

```python
# Filtrar modelos cuyo nombre comience con "Unicorn"
filter_string = "name LIKE 'Unicorn%'"

results = client.search_registered_models(filter_string=filter_string)
print(results)
```

---

## 4. Registro de Modelos (Creación de Versiones)

Existen tres formas principales de registrar un modelo (añadir una versión a un modelo registrado).

### 4.1. Usando `mlflow.register_model()` (Diapositivas 18-21)

Esta función registra un modelo ya existente (logueado en Tracking o en el sistema de archivos) bajo un nombre de modelo registrado.

- **Desde el sistema de archivos local:**
    ```python
    import mlflow
    mlflow.register_model(model_uri="./model", name="Unicorn")
    ```
- **Desde un run de MLflow Tracking:**
    ```python
    mlflow.register_model(model_uri="runs:/<run_id>/model", name="Unicorn")
    ```

**Salida típica:** Muestra que se crea una nueva versión (incrementada) y el estado es `READY`. La primera vez que se registra un modelo, se crea el modelo registrado automáticamente si no existe.

### 4.2. Durante el entrenamiento, con `log_model` (Diapositivas 24-25)

Puedes registrar el modelo directamente en el momento de loguearlo, usando el parámetro `registered_model_name`.

```python
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression

with mlflow.start_run():
    lr = LogisticRegression()
    lr.fit(X, y)
    mlflow.sklearn.log_model(lr, 
                             artifact_path="model", 
                             registered_model_name="Unicorn")
```

Esto crea automáticamente una nueva versión del modelo registrado "Unicorn" (o lo crea si no existe).

### 4.3. Desde la UI (implícitamente)

A través de la interfaz web también se puede registrar un modelo existente.

---

## 5. Gestión de Etapas (Stages)

### 5.1. Transición de Etapas (Diapositivas 35-38)

Para cambiar la etapa de una versión específica, se utiliza `transition_model_version_stage` del cliente.

```python
from mlflow import MlflowClient

client = MlflowClient()

# Transicionar la versión 3 del modelo "Unicorn" a Staging
client.transition_model_version_stage(
    name="Unicorn",
    version=3,
    stage="Staging"
)
```

**Salida:** Devuelve el objeto `ModelVersion` actualizado, con `current_stage='Staging'`.

Posteriormente, se puede promover a `Production` de la misma manera.

```python
client.transition_model_version_stage(
    name="Unicorn",
    version=3,
    stage="Production"
)
```

### 5.2. Visualización en la UI (Diapositivas 22-23, 37)

La interfaz de usuario de MLflow muestra:

- Lista de modelos registrados con sus últimas versiones.
- Al hacer clic en un modelo (ej. "Unicorn"), se ven todas las versiones, su etapa actual, fuente (run), etc.
- Desde la UI también se pueden cambiar las etapas manualmente.

---

## 6. Despliegue de Modelos desde el Registry

Una vez que un modelo está registrado y tiene una etapa asignada, se puede cargar o servir fácilmente.

### 6.1. Carga de Modelos por Etapa o Versión (Diapositivas 44-46)

MLflow proporciona una convención de URI para referirse a modelos registrados:

```
models:/<model_name>/<stage_or_version>
```

- **Por etapa:** `models:/Unicorn/Staging` (carga la última versión en esa etapa).
- **Por versión:** `models:/Unicorn/3` (carga la versión específica).

Ejemplo de carga con un flavor:

```python
import mlflow.sklearn

# Cargar el modelo que está en Staging
model = mlflow.sklearn.load_model("models:/Unicorn/Staging")

# Realizar predicciones
predictions = model.predict(data)
```

### 6.2. Servir un Modelo como API REST (Diapositivas 47-50)

El comando `mlflow models serve` también acepta URIs de modelos registrados.

```bash
mlflow models serve -m "models:/Unicorn/Production"
```

Esto levanta un servidor local (por defecto en `http://127.0.0.1:5000`) con los endpoints:

- `/ping` o `/health` para health checks.
- `/invocations` para predicciones.

#### Formato de las Peticiones (Diapositivas 48-50)

El endpoint `/invocations` acepta `Content-Type: application/json` o `application/csv`. El formato recomendado es `dataframe_split` (pandas DataFrame en orientación split).

Ejemplo de payload JSON:

```json
{
  "dataframe_split": {
    "columns": ["R&D Spend", "Administration", "Marketing Spend", "State"],
    "data": [[165349.20, 136897.80, 471784.10, 1]]
  }
}
```

Y se envía con `curl`:

```bash
curl http://127.0.0.1:5000/invocations \
    -H 'Content-Type: application/json' \
    -d '{
      "dataframe_split": {
        "columns": ["R&D Spend", "Administration", "Marketing Spend", "State"],
        "data": [[165349.20, 136897.80, 471784.10, 1]]
      }
    }'
```

---

## 7. Resumen del Ciclo de Vida con Model Registry (Diapositiva 2, 17, 41)

1. **Experimentación:** Se entrenan múltiples modelos y se loguean en Tracking.
2. **Registro:** El mejor modelo (o varios) se registra en el Model Registry, obteniendo una versión (ej. v1).
3. **Validación:** La versión se mueve a `Staging` para pruebas exhaustivas.
4. **Aprobación:** Tras validar, se transiciona a `Production`.
5. **Despliegue:** Las aplicaciones consumen el modelo desde la etapa `Production` usando la URI `models:/<model_name>/Production`.
6. **Actualización:** Un nuevo modelo mejorado se registra como v2, pasa por `Staging` y, si es exitoso, se promociona a `Production`. MLflow permite manejar este flujo de forma controlada.

---

## 8. 🚀 Perspectiva de Ingeniería (MLOps)

Como aspirante a **MLOps Engineer**, el Model Registry es una pieza fundamental para implementar **CI/CD en ML**:

- **Automatización:** Puedes integrar el registro y transición de etapas en pipelines de CI/CD. Por ejemplo, después de que un pipeline de entrenamiento valide un nuevo modelo, puede registrarlo automáticamente y dejarlo en `Staging`. Luego, un trigger manual o automático (si las métricas superan un umbral) lo promociona a `Production`.
- **Control de versiones:** Mantener un historial claro de qué modelo estuvo en producción y cuándo, facilita auditorías y rollbacks.
- **Separación de entornos:** Usar `Staging` para pruebas de integración y `Production` para tráfico real es análogo a los entornos en desarrollo de software.
- **Seguridad y gobernanza:** El Model Registry permite establecer permisos sobre quién puede cambiar etapas, evitando despliegues no autorizados.

---

## Conclusión

El **MLflow Model Registry** cierra el círculo entre la experimentación y la producción, proporcionando las herramientas necesarias para gestionar modelos de manera profesional, escalable y colaborativa. Dominar su uso te permitirá implementar flujos de MLOps robustos y confiables.