# MLflow Projects: Empaquetado Reproducible para Pipelines de ML

## 1. Introducción a MLflow Projects

MLflow Projects es un componente diseñado para empaquetar código de machine learning de una manera estandarizada y reproducible. Un proyecto MLflow es simplemente un directorio que contiene código y archivos de configuración que describen cómo ejecutarlo, sus dependencias y sus puntos de entrada.

### ¿Por qué necesitamos MLflow Projects?

En el desarrollo de ML, es común enfrentarse a problemas como:

- **Reproducibilidad:** El código que funciona en la máquina de un científico de datos no funciona en la de otro, o meses después.
- **Portabilidad:** Dificultad para ejecutar el mismo código en diferentes entornos (local, staging, producción, nube).
- **Colaboración:** Compartir un experimento implica compartir scripts, instrucciones manuales de instalación y archivos de configuración dispersos.

MLflow Projects resuelve estos problemas al empaquetar todo lo necesario en una estructura coherente.

---

## 2. Anatomía de un Proyecto MLflow

Un proyecto MLflow es un directorio que contiene al menos un archivo `MLproject` y el código fuente. Puede incluir también archivos de entorno y dependencias.

### 2.1. Estructura típica de un proyecto

```
project/
│
├── MLproject                 # Archivo de configuración principal (YAML)
├── train_model.py            # Código de entrenamiento
├── python_env.yaml           # Entorno virtual de Python (dependencias)
└── requirements.txt          # Lista de dependencias de Python
```

### 2.2. El archivo MLproject

Es el corazón del proyecto. Escrito en YAML, define metadatos y cómo ejecutar el código.

```yaml
name: salary_model
entry_points:
  main:
    command: "python train_model.py"
    python_env: python_env.yaml
```

- **`name`:** Nombre del proyecto (opcional pero recomendado).
- **`entry_points`:** Define los puntos de entrada (como funciones `main` en un programa). Cada punto de entrada tiene:
    - Un nombre (ej. `main`).
    - Un `command`: el comando a ejecutar (puede ser un script `.py`, `.sh`, etc.).
    - `python_env`: ruta al archivo de entorno (opcional si se usa `conda` o `virtualenv`).

### 2.3. Archivos de entorno

MLflow soporta múltiples formas de gestionar entornos:

- **`python_env.yaml`:** Especifica un entorno virtual de Python con dependencias.
- **`requirements.txt`:** Lista simple de paquetes pip (referenciado desde `python_env.yaml`).
- **`conda.yaml`:** Para entornos Conda.

Ejemplo de `python_env.yaml`:

```yaml
python: 3.10.8
build_dependencies:
  - pip
  - setuptools
  - wheel
dependencies:
  - -r requirements.txt
```

Ejemplo de `requirements.txt`:

```
mlflow
scikit-learn
pandas
```

### 2.4. Código de entrenamiento (`train_model.py`)

El script que realiza el entrenamiento. Utiliza MLflow Tracking para registrar automáticamente parámetros, métricas y modelos.

```python
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Cargar datos
df = pd.read_csv('Salary_predict.csv')
X = df[["experience", "age", "interview_score"]]
y = df[["Salary"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=0)

# Activar autologging
mlflow.sklearn.autolog()

# Entrenar modelo
lr = LinearRegression()
lr.fit(X_train, y_train)
```

Con `autolog()`, MLflow registra automáticamente:
- Parámetros del modelo.
- Métricas de entrenamiento (RMSE, R2, etc.).
- El modelo serializado.
- Versiones de librerías.

---

## 3. Ejecución de Proyectos MLflow

MLflow ofrece dos formas principales de ejecutar proyectos: mediante la API de Python y mediante la línea de comandos.

### 3.1. API de Python (`mlflow.projects.run`)

La función `mlflow.projects.run()` permite ejecutar un proyecto programáticamente.

```python
import mlflow

mlflow.projects.run(
    uri='./',                           # Ruta al directorio del proyecto
    entry_point='main',                 # Punto de entrada a ejecutar
    experiment_name='Salary Model',      # Experimento donde se logueará el run
    env_manager='virtualenv'             # Gestor de entorno: 'local' o 'virtualenv'
)
```

**Parámetros importantes:**
- **`uri`:** Puede ser una ruta local (`./`) o una URL de git (`git@github.com:user/project.git`).
- **`entry_point`:** El nombre del punto de entrada definido en `MLproject`.
- **`experiment_name`:** Nombre del experimento en MLflow Tracking. Si no existe, se crea automáticamente.
- **`env_manager`:** Controla cómo se maneja el entorno:
    - `local`: Usa el entorno actual (riesgo de conflicto).
    - `virtualenv`: Crea un entorno virtual aislado basado en `python_env.yaml` (recomendado para reproducibilidad).

**Salida típica:**
```
2023/04/02 14:33:23 INFO mlflow.projects: 'Salary Model' does not exist. Creating a new experiment
2023/04/02 14:33:23 INFO mlflow.utils.virtualenv: Installing python 3.10.8 if it does not exist
2023/04/02 14:33:23 INFO mlflow.utils.virtualenv: Creating a new environment...
2023/04/02 14:33:59 INFO mlflow.projects.backend.local: === Running command '... python train_model.py' in run with ID '562916d45aeb48ec84c1c393d6e3f5b6' ===
2023/04/02 14:34:34 INFO mlflow.projects: === Run (ID '562916d45aeb48ec84c1c393d6e3f5b6') succeeded ===
```

### 3.2. Línea de comandos (`mlflow run`)

El comando `mlflow run` es el equivalente en terminal.

```bash
mlflow run ./ --entry-point main --experiment-name "Salary Model" --env-manager virtualenv
```

**Opciones:**
- `--entry-point`: Punto de entrada a ejecutar.
- `--experiment-name`: Experimento de destino.
- `--env-manager`: `local` o `virtualenv`.
- `-P`: Para pasar parámetros (ver sección 4).

Al ejecutarse, MLflow:
1. Verifica o crea el entorno virtual.
2. Instala las dependencias.
3. Ejecuta el comando definido.
4. Loguea todo en MLflow Tracking.

---

## 4. Parametrización de Proyectos

Para hacer los proyectos flexibles y reutilizables, se pueden definir parámetros en el archivo `MLproject`.

### 4.1. Definición de parámetros en MLproject

```yaml
name: salary_model
python_env: python_env.yaml
entry_points:
  main:
    parameters:
      n_jobs_param:
        type: int
        default: 1
      fit_intercept_param:
        type: bool
        default: True
    command: "python train_model.py {n_jobs_param} {fit_intercept_param}"
```

- **`type`:** Puede ser `int`, `float`, `bool`, `string` (por defecto). Ayuda a MLflow a validar y convertir los valores.
- **`default`:** Valor por defecto si no se especifica.

### 4.2. Modificación del script para aceptar parámetros

El script `train_model.py` debe leer los argumentos de línea de comandos, por ejemplo con `sys.argv`:

```python
import sys
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
# ... (carga de datos, etc.)

# Leer parámetros
n_jobs_param = int(sys.argv[1])
fit_intercept_param = bool(sys.argv[2])

# Entrenar modelo con parámetros
lr = LinearRegression(n_jobs=n_jobs_param, fit_intercept=fit_intercept_param)
lr.fit(X_train, y_train)
```

### 4.3. Ejecución con parámetros

**Desde la API de Python:**

```python
mlflow.projects.run(
    uri='./',
    entry_point='main',
    experiment_name='Salary Model',
    parameters={
        'n_jobs_param': 2,
        'fit_intercept_param': False
    }
)
```

**Desde la línea de comandos:**

```bash
mlflow run ./ \
    --entry-point main \
    --experiment-name "Salary Model" \
    -P n_jobs_param=3 \
    -P fit_intercept_param=True
```

El comando generado internamente será:
```bash
python train_model.py 2 False
```

Y MLflow registrará estos valores como parámetros del run.

---

## 5. Creación de Workflows Multi-paso

MLflow Projects permite definir múltiples puntos de entrada y encadenarlos para crear flujos de trabajo (workflows) complejos.

### 5.1. Definición de múltiples steps en MLproject

```yaml
name: project_name
python_env: python_env.yaml
entry_points:
  step_1:
    command: "python train_model.py"
  step_2:
    parameters:
      run_id:
        type: str
        default: None
    command: "python evaluate_model.py {run_id}"
```

- `step_1`: Entrena el modelo.
- `step_2`: Evalúa el modelo, tomando como entrada el `run_id` del paso anterior.

### 5.2. Encadenamiento con la API de Python

```python
import mlflow

# Ejecutar step_1
step_1 = mlflow.projects.run(
    uri='./',
    entry_point='step_1'
)

# Obtener el run_id del primer paso
step_1_run_id = step_1.run_id

# Ejecutar step_2, pasando el run_id como parámetro
step_2 = mlflow.projects.run(
    uri='./',
    entry_point='step_2',
    parameters={'run_id': step_1_run_id}
)
```

### 5.3. Gestión de ejecuciones

El objeto devuelto por `mlflow.projects.run()` proporciona métodos útiles:

- **`run_id`:** ID de la ejecución.
- **`wait()`:** Espera a que la ejecución termine.
- **`get_status()`:** Obtiene el estado actual.
- **`cancel()`:** Termina la ejecución en curso.

```python
step_1 = mlflow.projects.run(uri='./', entry_point='step_1')
print(step_1.run_id)               # Muestra el ID
step_1.wait()                       # Espera a que termine
print(step_1.get_status())          # Ej. "FINISHED"
```

### 5.4. Beneficios de los workflows con MLflow Projects

- **Modularidad:** Cada paso (entrenamiento, evaluación, validación) es independiente.
- **Reproducibilidad:** Cada paso se ejecuta en el mismo entorno controlado.
- **Trazabilidad:** Los `run_id` conectan los pasos, creando un linaje completo del modelo.

---

## 6. Resumen: MLflow Projects en el Ciclo de Vida de MLOps

| Problema | Solución con MLflow Projects |
| :--- | :--- |
| **"En mi máquina funciona"** | Entornos aislados y reproducibles (`virtualenv`). |
| **Código desorganizado** | Estructura estándar con `MLproject` y puntos de entrada. |
| **Dependencias no documentadas** | Archivos `python_env.yaml` y `requirements.txt`. |
| **Ejecución en diferentes entornos** | Mismo comando `mlflow run` funciona en local, remoto o nube. |
| **Flujos complejos manuales** | Workflows multi-paso automatizados y encadenados. |
| **Pérdida de trazabilidad** | Cada paso se loguea en Tracking y se conecta mediante `run_id`. |

MLflow Projects, junto con Tracking, Models y Model Registry, completa el ecosistema para gestionar el ciclo de vida completo de ML de manera profesional, reproducible y escalable.

---

## Conclusión

MLflow Projects es la herramienta que transforma scripts dispersos en pipelines reproducibles y compartibles. Al estandarizar la estructura, el entorno y la ejecución, permite a los equipos de MLOps mover modelos del desarrollo a producción con confianza y eficiencia.