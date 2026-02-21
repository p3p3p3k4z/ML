# Apuntes de MLflow: Introducción a MLflow Models

MLflow Models es un componente clave del ecosistema MLflow que estandariza el empaquetado, la gestión y el ciclo de vida de los modelos de machine learning, facilitando su uso en diferentes entornos y herramientas.

## 1. Flavors (Sabores): La Clave de la Interoperabilidad

Un "flavor" en MLflow es una convención que permite que una herramienta de ML sepa cómo guardar y cargar un modelo. Es la capa de abstracción que hace que un modelo de, por ejemplo, Scikit-learn, pueda ser utilizado como si fuera una función Python genérica.

### 1.1. Flavors Integrados (Built-In Flavors)

MLflow incluye flavors para las bibliotecas de ML más populares, lo que simplifica enormemente el trabajo, ya que no necesitas escribir código personalizado para guardar o cargar estos modelos.

- **Uso Común:** `scikit-learn (sklearn)`, `TensorFlow (tensorflow)`, `Keras (keras)`, `PyTorch (pytorch)`, `XGBoost (xgboost)`.
- **Para Interoperabilidad y Serving:** `Python Function (python_function)`, `ONNX (onnx)`, `MLeap (mleap)`.
- **Para Otros Ecosistemas:** `R Function (crate)`, `Spark MLlib (spark)`, `H2O (h₂O)`, `MXNet Gluon (gluon)`.

**Concepto Clave:**
> "Los flavors simplifican la necesidad de código personalizado." Puedes importar un flavor específico desde el módulo de MLflow y trabajar con él de manera nativa.

```python
import mlflow
import mlflow.sklearn  # Importa el flavor de scikit-learn
import mlflow.tensorflow # Importa el flavor de TensorFlow
```

---

## 2. Autologging: El Poder de la Automatización

`autolog()` es una de las características más potentes de MLflow. Con una sola línea de código, MLflow automáticamente registra parámetros, métricas, y el modelo mismo durante el entrenamiento, sin necesidad de intervención manual.

### 2.1. Sintaxis y Uso
```python
import mlflow
from sklearn.linear_model import LinearRegression

# Habilita el autologging para scikit-learn
mlflow.sklearn.autolog()

# Entrena el modelo - MLflow hace su magia automáticamente
lr = LinearRegression()
lr.fit(X, y)  # <-- El modelo se loguea automáticamente en esta línea
```

### 2.2. ¿Qué se Registra Automáticamente?

- **Parámetros (Parameters):** Todos los hiperparámetros del modelo.
    - Comunes: `fit_intercept`, `normalize`, `copy_X`, `n_jobs`.
    - Se obtienen internamente con `MODEL.get_params()`.
- **Métricas (Metrics):** Las métricas de rendimiento más comunes para el tipo de modelo.
    - **Regresión:** `mean_squared_error`, `root_mean_squared_error`, `mean_absolute_error`, `r2_score`.
    - **Clasificación:** `precision_score`, `recall_score`, `f1_score`, `accuracy_score`.
- **Artefactos (Artifacts):** El modelo en sí se guarda como un artefacto en una estructura de directorio estandarizada.

---

## 3. Formato de Almacenamiento de MLflow Models

Cuando MLflow guarda un modelo (automáticamente o mediante `save_model`), crea una estructura de directorio específica. Esto garantiza la **reproducibilidad** (uno de los pilares de MLOps).

### 3.1. Estructura de Directorios de un Modelo
```
model/
│
├── MLmodel               # El archivo de metadatos (YAML). ¡Es el corazón del modelo!
├── model.pkl             # El modelo serializado en pickle (u otro formato según el flavor)
├── requirements.txt      # Dependencias de Python necesarias para ejecutar el modelo
└── python_env.yaml       # Entorno virtual de Conda (alternativa a requirements.txt)
```

### 3.2. El Archivo `MLmodel`: El Manifiesto del Modelo
Este archivo contiene toda la información necesaria para cargar y usar el modelo de manera correcta y reproducible. Es un archivo en formato YAML.

**Contenido típico de `MLmodel`:**
```yaml
artifact_path: model
flavors:
  python_function:
    env:
      virtualenv: python_env.yaml
    loader_module: mlflow.sklearn
    model_path: model.pkl
    predict_fn: predict
    python_version: 3.10.8
  sklearn:
    code: null
    pickled_model: model.pkl
    serialization_format: cloudpickle
    sklearn_version: 1.1.3
mlflow_version: 2.1.1
model_uuid: 288102e3a400453d96241a1a7b01667e
run_id: e84a122920de4bdeaedb54146deeb429
```
- **`flavors`:** Define cómo cargar el modelo en diferentes contextos. El flavor `python_function` es el más genérico, mientras que `sklearn` es el específico.
- **`run_id`:** Conecta el modelo con la ejecución específica en MLflow Tracking que lo generó.
- **`model_uuid`:** Un identificador único para el modelo.
- **`mlflow_version`:** La versión de MLflow usada para guardarlo, crucial para la compatibilidad.

---

## 4. La API del Modelo: Guardar, Cargar y Gestionar

MLflow proporciona una API simple y unificada para la gestión del ciclo de vida del modelo.

### 4.1. Operaciones Principales
- **Guardar (Save):** Guarda el modelo en el sistema de archivos local.
- **Loguear (Log):** Guarda el modelo como un artefacto dentro de MLflow Tracking (asociado a un `run` específico).
- **Cargar (Load):** Carga un modelo desde el sistema de archivos local o desde MLflow Tracking.

### 4.2. Funciones Clave del Flavor (Ej. `mlflow.sklearn`)
```python
import mlflow.sklearn

# Guardar en el sistema de archivos local
mlflow.sklearn.save_model(model, "ruta/local/al/modelo")

# Loguear en MLflow Tracking (durante un run activo)
mlflow.sklearn.log_model(model, "ruta_del_artefacto")

# Cargar desde cualquier fuente soportada
modelo_cargado = mlflow.sklearn.load_model("runs:/<run_id>/ruta_del_artefacto")
```

### 4.3. URIs de Modelo (Cómo Referenciar un Modelo)
MLflow utiliza URIs para localizar modelos de manera unificada.

- **Sistema de Archivos Local:**
    - Ruta relativa: `"ruta/relativa/al/modelo"`
    - Ruta absoluta: `"/Users/me/ruta/absoluta/al/modelo"`
- **MLflow Tracking:**
    - Formato: `"runs:/<run_id>/ruta/relativa/del/artefacto"`
    - Ejemplo: `"runs:/e84a1229.../model"`
- **Almacenamiento en la Nube:**
    - **S3:** `"s3://mi_bucket/ruta/al/modelo"`

### 4.4. Flujo de Trabajo con `last_active_run`
Una forma común de trabajar es obtener el ID de la última ejecución para cargar el modelo justo después de entrenarlo.

```python
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression

# --- Entrenamiento y Logueo ---
mlflow.sklearn.autolog()
lr = LogisticRegression()
lr.fit(X, y)

# --- Obtención del ID del último run ---
run = mlflow.last_active_run()
run_id = run.info.run_id

# --- Carga del modelo usando el run_id ---
modelo_uri = f"runs:/{run_id}/model"  # 'model' es el artifact_path por defecto de autolog
modelo_cargado = mlflow.sklearn.load_model(modelo_uri)
```

---

## 5. Modelos Personalizados (Custom Models) con `pyfunc`

Cuando necesitas lógica que va más allá de un simple modelo predictivo (como preprocesamiento, postprocesamiento, o usar librerías no soportadas por un flavor específico), el flavor **`python_function`** (`pyfunc`) es la solución. Te permite empaquetar cualquier objeto Python como un modelo de MLflow.

### 5.1. Casos de Uso Típicos
- **NLP:** Incluir tokenizadores y pipelines de texto.
- **Clasificación:** Incluir un `LabelEncoder` para transformar las etiquetas.
- **Pre/Post-procesamiento:** Normalizar la entrada, validar datos, o formatear la salida de una manera específica.
- **Modelos sin un flavor built-in:** Cualquier librería o lógica personalizada.

### 5.2. La Clase `PythonModel`
Para crear un modelo personalizado, debes crear una clase que herede de `mlflow.pyfunc.PythonModel` e implementar dos métodos clave:

1.  **`load_context(self, context)`** (Opcional): Se ejecuta una sola vez cuando el modelo se carga desde el disco. Es el lugar ideal para cargar artefactos pesados como modelos de ML, tokenizadores, etc. El objeto `context` proporciona acceso a los `artifacts`.
2.  **`predict(self, context, model_input)`** (Obligatorio): Se ejecuta cada vez que se hace una predicción. `model_input` es un objeto pandas DataFrame. Aquí defines la lógica completa de inferencia.

```python
import mlflow.pyfunc
import mlflow.sklearn
import pandas as pd

class ModeloConPreprocesamiento(mlflow.pyfunc.PythonModel):
    
    def load_context(self, context):
        # Carga el modelo de scikit-learn desde los artifacts
        self.modelo_sklearn = mlflow.sklearn.load_model(context.artifacts["mi_modelo_sklearn"])
        # Podrías cargar un tokenizador, encoder, etc.
        # self.tokenizador = joblib.load(context.artifacts["tokenizador"])
        
    def predict(self, context, model_input):
        # Aplica preprocesamiento a model_input (un DataFrame)
        # datos_procesados = self.tokenizador.transform(model_input)
        
        # Realiza la predicción con el modelo cargado
        predicciones = self.modelo_sklearn.predict(model_input)
        
        # Aplica postprocesamiento (ej. convertir índices a nombres de clase)
        # resultados = self.encoder.inverse_transform(predicciones)
        return predicciones
```

### 5.3. Guardar y Cargar un Modelo Personalizado

- **Guardar/Loguear:** Al guardar, debes proporcionar la clase y, si es necesario, un diccionario de `artifacts` (referencias a otros modelos o archivos).
    ```python
    # Diccionario con las rutas a los artifacts que necesitará el modelo
    artifacts = {"mi_modelo_sklearn": "runs:/<run_id>/modelo_base"}
    
    mlflow.pyfunc.log_model(
        artifact_path="modelo_con_prepro",
        python_model=ModeloConPreprocesamiento(),
        artifacts=artifacts
    )
    ```
- **Cargar:** Se carga igual que cualquier otro modelo de MLflow.
    ```python
    modelo_cargado = mlflow.pyfunc.load_model("runs:/<otro_run_id>/modelo_con_prepro")
    predicciones = modelo_cargado.predict(dataframe_de_entrada)
    ```

---

## 6. Evaluación de Modelos con `mlflow.evaluate()`

MLflow ofrece una función integrada para evaluar modelos de manera automática y generar artefactos de evaluación detallados.

### 6.1. Uso Básico
```python
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# ... (preparación de datos y entrenamiento) ...
X_train, X_test, y_train, y_test = train_test_split(X, y)
lr = LinearRegression()
lr.fit(X_train, y_train)

# Preparar el dataset de evaluación (debe incluir las features y la columna target)
eval_data = X_test.copy()
eval_data["target_real"] = y_test

# Evaluar el modelo
mlflow.evaluate(
    model="runs:/<run_id_del_modelo>/model",  # URI del modelo
    data=eval_data,                            # DataFrame con datos de prueba
    targets="target_real",                      # Nombre de la columna con el target real
    model_type="regressor"                      # Tipo de modelo: "regressor" o "classifier"
)
```
### 6.2. Resultados de la Evaluación
Además de las métricas estándar, `mlflow.evaluate()` puede generar artefactos de diagnóstico avanzados, como gráficos de importancia de características (SHAP), que se guardan automáticamente en el run y son visibles en la UI de MLflow.

- **Métricas:** Se loguean en el run actual.
- **Artefactos:** Se guardan gráficos como:
    - **SHAP:** Explicabilidad del modelo.
    - Curvas de error, matrices de confusión (para clasificación), etc.

---

## 7. Model Serving: Sirviendo Modelos como API REST

Una de las ventajas más importantes del empaquetado estandarizado de MLflow es la capacidad de servir cualquier modelo como un servicio REST API con un solo comando.

### 7.1. El Comando `mlflow models serve`
```bash
mlflow models serve --help
```
Este comando levanta un servidor web local (usando Gunicorn) que expone el modelo a través de una API REST.

### 7.2. URI del Modelo a Servir
Al igual que con `load_model`, puedes servir modelos desde cualquier fuente:
```bash
# Desde el sistema de archivos local
mlflow models serve -m ruta/local/al/modelo

# Desde MLflow Tracking (usando el run_id)
mlflow models serve -m runs:/e84a1229.../artifacts/model

# Desde AWS S3
mlflow models serve -m s3://mi_bucket/ruta/al/modelo
```

### 7.3. Endpoints de la API
Una vez que el servidor está corriendo (por defecto en `http://127.0.0.1:5000`), expone los siguientes endpoints:

- **`/ping` o `/health`:** Para chequeos de salud del servidor.
- **`/version`:** Para obtener la versión de MLflow.
- **`/invocations`:** El endpoint principal para hacer predicciones (scoring).

### 7.4. Formato de las Peticiones (Payload)
El servidor espera datos en un formato específico, basado en pandas DataFrames.

- **Content-Type:** Debe ser `application/json` o `application/csv`.
- **Formato JSON recomendado: `dataframe_split`**:
    Este formato separa las columnas de los datos, lo cual es muy eficiente y claro.
    ```json
    {
      "dataframe_split": {
        "columns": ["sexo", "edad", "peso"],
        "data": [
          ["hombre", 23, 160],
          ["mujer", 33, 120]
        ]
      }
    }
    ```
- **Formato JSON alternativo: `dataframe_records`**:
    Es un formato más "hablado" pero puede ser menos eficiente para datos tabulares grandes.
    ```json
    {
      "dataframe_records": [
        {"sexo": "hombre", "edad": 23, "peso": 160},
        {"sexo": "mujer", "edad": 33, "peso": 120}
      ]
    }
    ```
- **Formato CSV:** Enviar el contenido de un CSV directamente en el body de la petición.

### 7.5. Ejemplo de Petición con `curl`
```bash
curl http://127.0.0.1:5000/invocations \
    -H 'Content-Type: application/json' \
    -d '{
      "dataframe_split": {
        "columns": ["sexo", "edad", "peso"],
        "data": [["hombre", 23, 160]]
      }
    }'
```
La respuesta será un JSON con las predicciones:
```json
{ "predictions": [1] }
```

---

## Resumen: MLflow Models en el Ciclo de Vida de MLOps

| Etapa MLOps | Función de MLflow Models | Beneficio Clave |
| :--- | :--- | :--- |
| **Desarrollo** | `autolog()` y `log_model()` | Registro automático y trazabilidad de modelos y métricas. |
| **Empaquetado** | Flavors (`sklearn`, `tensorflow`, `pyfunc`) | Estandarización y reproducibilidad del modelo. |
| **Gestión** | `save_model()`, `load_model()` | Ciclo de vida unificado (local, tracking server, nube). |
| **Evaluación** | `mlflow.evaluate()` | Evaluación automática y generación de reportes de explicabilidad. |
| **Despliegue** | `mlflow models serve` | Servir cualquier modelo como API REST con un solo comando. |
