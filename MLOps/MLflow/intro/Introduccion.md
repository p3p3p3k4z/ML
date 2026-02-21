# Apuntes Definitivos de MLflow: Gestión del Ciclo de Vida de ML

## 1. ¿Qué es MLflow? (Visión General)

MLflow es una **plataforma de código abierto** diseñada para gestionar el ciclo de vida completo de Machine Learning (ML). Su objetivo es introducir orden y estandarización en un flujo de trabajo que, de otra forma, puede volverse caótico, especialmente a medida que los proyectos escalan.

### El Ciclo de Vida que gestiona MLflow (Contexto)

- **Planificación:** Definición del problema de negocio.
- **Ingeniería de Datos:** Recolección, limpieza y preparación de datos.
- **Ingeniería del Modelo:** Diseño, entrenamiento y ajuste de hiperparámetros.
- **Evaluación del Modelo:** Pruebas de rendimiento y validación.
- **Despliegue del Modelo:** Puesta en producción del modelo.
- **Operaciones y Monitoreo:** Gestión de la infraestructura y vigilancia continua del rendimiento del modelo en producción.

---

## 2. Los Desafíos que resuelve MLflow (El "Por qué")

El desarrollo de ML se enfrenta a tres desafíos fundamentales que MLflow aborda directamente, tal como se indica en las diapositivas:

1.  **Seguimiento (Tracking):**
    - **Problema:** Es complicado y propenso a errores llevar el registro manual de cientos de experimentos, sus parámetros (hiperparámetros) y las métricas resultantes (accuracy, loss, etc.).
    - **Solución de MLflow:** Proporciona un sistema de registro automático y manual para asociar cada modelo con sus metadatos.

2.  **Reproducibilidad:**
    - **Problema:** Es difícil, o a veces imposible, recrear exactamente el mismo modelo si no se tiene un registro preciso del código, las versiones de las librerías, los datos y la configuración del entorno (plataformas, espacios de trabajo) utilizados.
    - **Solución de MLflow:** Permite empaquetar el código y las dependencias, asegurando que un modelo pueda ser reentrenado de manera idéntica en cualquier momento y lugar.

3.  **Despliegue (Deployment):**
    - **Problema:** Existe una gran variedad de opciones de despliegue (servidores REST, motores de batch, móviles, etc.) y una falta de estándares para empaquetar modelos, lo que dificulta el paso de la fase de desarrollo a la producción.
    - **Solución de MLflow:** Introduce un formato estándar para empaquetar modelos (MLflow Models) que puede ser entendido por múltiples herramientas de despliegue.

---

## 3. Los Cuatro Componentes Principales de MLflow

MLflow se estructura en cuatro módulos especializados, cada uno diseñado para abordar una parte específica del ciclo de vida. La diapositiva 5 los resume perfectamente.

| Componente | Función Principal | Analogía |
| :--- | :--- | :--- |
| **MLflow Tracking** | Registrar y consultar experimentos (parámetros, métricas, artefactos). | El "diario de laboratorio" de un científico. |
| **MLflow Projects** | Empaquetar código de ML de forma reproducible. | El "plano" y las "instrucciones de montaje". |
| **MLflow Models** | Estandarizar el formato de los modelos para el despliegue. | El "producto empaquetado" listo para su envío. |
| **Model Registry** | Gestionar, versionar y controlar el estado de los modelos. | El "almacén central" con control de versiones. |

### A. MLflow Tracking (Seguimiento)

Es el componente central para la experimentación. Las diapositivas 11-22 profundizan en su uso.

- **Registro:** Permite grabar:
    - **Parámetros:** Clave-valor con entradas como `n_jobs=1` o `fit_intercept=False`. (`log_param`, `log_params`).
    - **Métricas:** Clave-valor con resultados numéricos como `accuracy=0.90` o `loss=0.50`. (`log_metric`, `log_metrics`).
    - **Artefactos:** Archivos de cualquier tipo generados durante el run: modelos serializados (`.pkl`), gráficos, archivos de código fuente (`train.py`), etc. (`log_artifact`, `log_artifacts`).
- **Organización por Runs y Experimentos:**
    - **Run (Ejecución):** Corresponde a un único entrenamiento de modelo. MLflow asigna un ID único (`run_id`).
    - **Experimento:** Es un contenedor lógico para agrupar runs relacionados (ej. "LR Experiment" para pruebas de regresión logística).
- **API y Cliente:** Se puede interactuar con Tracking de dos maneras:
    - **Módulo `mlflow`:** Funciones de alto nivel como `mlflow.start_run()`, `mlflow.log_param()`.
    - **Cliente (`MlflowClient`):** Proporciona un control más granular para crear, borrar y etiquetar experimentos de forma programática.
- **Interfaz de Usuario (UI):** Se lanza con `mlflow ui` y se accede en `http://localhost:5000`. Permite visualizar, comparar y buscar runs de forma gráfica.

### B. MLflow Projects (Proyectos)

- **Función:** Empaquetar código de ML en una forma reutilizable y reproducible. Un proyecto es simplemente un directorio con código y un archivo `MLproject` (o `conda.yaml`/`requirements.txt`) que describe sus dependencias y puntos de entrada.
- **Beneficio:** Permite ejecutar el mismo código en diferentes entornos (local, remoto, nube) sin cambios, garantizando la **repetibilidad**.

### C. MLflow Models (Modelos)

- **Función:** Definir un formato estándar para empaquetar modelos de ML, independientemente de la librería con la que se hayan entrenado.
- **Flavors (Sabores):** Un modelo puede ser visto desde diferentes perspectivas. Por ejemplo, un modelo entrenado con scikit-learn tiene un "sabor" `sklearn` (para ser cargado por scikit-learn) y un "sabor" `python_function` (para ser cargado como una función Python genérica para inferencia). Esto es clave para el despliegue.

### D. Model Registry (Registro de Modelos)

- **Función:** Es un almacén centralizado y colaborativo para gestionar el ciclo de vida completo de un modelo.
- **Versionado:** Cada modelo registrado puede tener múltiples versiones (v1, v2, v3...).
- **Etapas (Stages):** Permite asignar una etapa a cada versión del modelo, como `Staging` (para pruebas), `Production` (para servir tráfico en vivo) o `Archived`. Esto facilita el control de qué modelo está en producción y la promoción controlada de nuevos modelos.

---

## 4. Implementación Técnica: Trabajando con Tracking y Runs

Las diapositivas 8-31 ofrecen ejemplos de código muy valiosos que detallan la interacción con MLflow.

### 4.1. Gestión de Experimentos (Diapositivas 8-10)
```python
import mlflow

# Crear un nuevo experimento
mlflow.create_experiment("Insurance Experiment")

# Establecer una etiqueta (tag) para el experimento
mlflow.set_experiment_tag("framework", "scikit-learn")

# Establecer el experimento activo para los siguientes runs
mlflow.set_experiment("Insurance Experiment")
```

### 4.2. Inicio y Fin de un Run (Diapositivas 14-16)
```python
# Iniciar un run. Todo lo que se loguee a continuación pertenecerá a este run.
with mlflow.start_run():
    # Código de entrenamiento...
    lr = LogisticRegression(n_jobs=1)
    lr.fit(X_train, y_train)
    score = lr.score(X_test, y_test)

    # Loguear parámetros, métricas y artefactos
    mlflow.log_param("n_jobs", 1)
    mlflow.log_metric("accuracy", score)
    mlflow.log_artifact("train_code.py") # Guardar el script usado

# El run se cierra automáticamente al salir del bloque 'with'
```
> **Nota:** La función `mlflow.start_run()` devuelve un objeto `ActiveRun` que contiene metadatos como el `run_id`, `experiment_id`, etc., que se pueden inspeccionar.

### 4.3. Consulta Avanzada de Runs (Diapositivas 23-31)

Una de las características más potentes para MLOps es la capacidad de buscar y filtrar runs programáticamente, devolviendo los resultados como un DataFrame de Pandas para su análisis.

```python
import mlflow
import pandas as pd

# Definir un filtro para encontrar runs con buena métrica
f1_filter = "metrics.f1_score > 0.60"

# Buscar runs en un experimento específico, ordenados por precisión descendente
runs_df: pd.DataFrame = mlflow.search_runs(
    experiment_names=["Insurance Experiment"],
    filter_string=f1_filter,
    order_by=["metrics.precision_score DESC"]
)

# El DataFrame resultante tiene una columna por cada parámetro, métrica y tag.
print(runs_df.head())
```

**Estructura del DataFrame de Runs (Diapositiva 27):**
El DataFrame devuelto por `search_runs` es extremadamente útil para análisis y comparaciones. Contiene columnas como:
- `run_id`, `experiment_id`, `status`.
- `metrics.<nombre_metrica>` (ej. `metrics.accuracy`, `metrics.f1_score`).
- `params.<nombre_parametro>` (ej. `params.n_estimators`, `params.max_depth`).
- `tags.<nombre_tag>` (ej. `tags.mlflow.user`).
- `start_time`, `end_time`, `artifact_uri`.

---

## 5. Integraciones y Ecosistema

Como bien señalas, una de las mayores fortalezas de MLflow es su capacidad de integración. Esto no es un accidente, sino un diseño fundamental. La diapositiva 3 y la documentación oficial lo confirman.

- **Frameworks de ML:** Scikit-learn, TensorFlow, PyTorch, Keras, XGBoost, LightGBM, Spark MLlib.
- **Lenguajes:** Python (principal), R, Java.
- **Formatos y Estándares:** ONNX, MLeap.
- **Almacenamiento de Artefactos:** Sistema de archivos local, AWS S3, Azure Blob Storage, Google Cloud Storage, SFTP server, etc.
- **Bases de Datos para el Backend:** SQLite (por defecto), MySQL, PostgreSQL, MSSQL.

---

## 6. 🚀 Perspectiva de Ingeniería (MLOps/DevOps) - **El Valor para tu Rol**

Tu análisis final es el más importante para tu objetivo profesional. MLflow no es solo una herramienta para científicos de datos; es la columna vertebral de la infraestructura de MLOps. Aquí tienes una visión más detallada de tu rol con MLflow:

- **Infraestructura del Tracking Server:** Tu responsabilidad es desplegar y mantener el servidor de MLflow (Tracking Server) de forma robusta y escalable. Esto implica elegir el backend apropiado (una base de datos como PostgreSQL para metadatos) y el almacenamiento de artefactos (un bucket S3, por ejemplo) para un entorno de producción.
- **Gestión del Model Registry:** Debes configurar y gestionar los permisos y el flujo de aprobación en el Model Registry. Por ejemplo, asegurarte de que solo las versiones de modelo etiquetadas como `Production` tengan acceso a los endpoints de inferencia de alto rendimiento. Integrarías esto con pipelines de CI/CD para que un nuevo modelo en `Staging` pueda ser desplegado automáticamente en un entorno de prueba.
- **Automatización y CI/CD:** Integrarás MLflow en los pipelines de CI/CD. Por ejemplo, un pipeline de entrenamiento que corre en Jenkins o GitHub Actions puede usar `mlflow.start_run()` para loguear sus resultados. Un pipeline de despliegue puede consultar el Model Registry para obtener la última versión del modelo en `Production` y desplegarlo.
- **Monitoreo de la Salud del Sistema:** Más allá de monitorear el rendimiento del modelo, monitorearás la salud del propio servidor de MLflow: espacio en disco para artefactos, latencia de la base de datos, tasa de éxito de logging, etc.

---

## Resumen Visual del Flujo de Trabajo con MLflow

1.  **Científico de Datos:** Experimenta localmente, usando `mlflow.start_run()` y `autolog()`. MLflow Tracking guarda todo.
2.  **MLflow Tracking Server:** Recibe y almacena los metadatos (params, metrics) y los artefactos (modelos, plots).
3.  **Revisión:** El científico (o un proceso automático) revisa los runs en la UI y selecciona el mejor modelo.
4.  **Registro:** El modelo seleccionado se registra en el **Model Registry** con una nueva versión.
5.  **Promoción:** Se cambia la etapa del modelo de `None` a `Staging` (para pruebas) y luego a `Production`.
6.  **Despliegue:** Una herramienta de CI/CD o un script de despliegue consulta al Model Registry por la versión en `Production` (`models:/<model_name>/Production`) y la sirve como API con `mlflow models serve`.
