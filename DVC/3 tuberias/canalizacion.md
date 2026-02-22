# Apuntes de DVC: Pipelines, Ejecución y Evaluación de Modelos

## 1. Organización del Código: De Prototipo a Producción

### 1.1. Código de prototipado vs. código de producción

En el desarrollo de proyectos de Machine Learning, es común comenzar con código de **prototipado** (experimentación rápida en notebooks o scripts simples). Sin embargo, este código suele tener características que lo hacen inadecuado para producción:

- **No es reproducible:** Depende de ejecuciones manuales y estado de la memoria.
- **Poco modular:** Muchas funciones monolíticas, código duplicado.
- **Propenso a errores:** Sin pruebas, con dependencias implícitas.
- **Parámetros hardcodeados:** Dificulta la experimentación y el versionado.

### 1.2. Características del buen código de producción

Para que un pipeline de ML sea robusto y mantenible, debe cumplir:

- **Reproducible:** El mismo código debe producir los mismos resultados en diferentes entornos y momentos.
- **Modular:** Dividido en funciones o módulos independientes, testables y reutilizables.
- **Consistente:** Los parámetros (hiperparámetros, rutas, configuraciones) deben estar centralizados en un solo lugar, no dispersos en el código.

### 1.3. Archivo de parámetros: `params.yaml`

DVC promueve el uso de un archivo `params.yaml` para centralizar todos los parámetros del proyecto. Este archivo sigue el formato YAML y puede contener:

- Valores escalares (enteros, flotantes, cadenas)
- Listas (arrays)
- Diccionarios anidados
- Comentarios (con `#`)

**Ejemplo de `params.yaml`:**
```yaml
# Parámetros de preprocesamiento
preprocess:
  target_column: "RainTomorrow"
  categorical_features:
    - "Location"
    - "WindGustDir"

# Parámetros de entrenamiento y evaluación
train_and_evaluate:
  rfc_params:
    n_estimators: 2
    max_depth: 5
  test_size: 0.2
```

**Ventajas:**
- Los parámetros se leen desde el código (ej. con `yaml.safe_load`).
- Se pueden versionar con Git.
- DVC puede rastrear cambios en estos parámetros y usarlos para invalidar etapas del pipeline.

### 1.4. Modularización del código

Separar la lógica en módulos independientes facilita el mantenimiento y las pruebas.

**Ejemplo de estructura modular:**

```
project/
├── params.yaml
├── dvc.yaml
├── src/
│   ├── preprocess.py      # funciones de limpieza y transformación
│   ├── train.py           # entrenamiento de modelos
│   ├── evaluate.py        # métricas y evaluación
│   └── utils.py           # utilidades comunes
└── notebooks/             # (opcional) para análisis exploratorio
```

**Ejemplo de función modular en `evaluate.py`:**
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(model, X_test, y_test):
    """Evalúa un modelo y retorna un diccionario con métricas."""
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average='weighted'),
        "recall": recall_score(y_test, y_pred, average='weighted'),
        "f1_score": f1_score(y_test, y_pred, average='weighted')
    }
    return metrics
```

---

## 2. Pipelines en DVC: Definición y Visualización

### 2.1. ¿Qué es un pipeline en DVC?

Un **pipeline** en DVC es una secuencia de etapas que definen el flujo de trabajo de Machine Learning, incluyendo sus dependencias (código, datos, parámetros) y salidas (modelos, métricas, gráficos). El pipeline se define en un archivo `dvc.yaml` y se versiona con Git.

**Componentes de una etapa (stage):**
- **`cmd`**: comando a ejecutar.
- **`deps`**: dependencias (scripts, datos de entrada).
- **`params`**: parámetros del archivo `params.yaml` que esta etapa utiliza.
- **`outs`**: salidas (archivos generados: datos procesados, modelos, etc.).
- **`metrics`**: archivos de métricas (especialmente para comparar experimentos).
- **`plots`**: archivos para gráficos (imágenes, CSV para visualización).

### 2.2. Creación de etapas con `dvc stage add`

El comando `dvc stage add` genera automáticamente la entrada en `dvc.yaml`.

**Ejemplo: etapa de preprocesamiento**
```bash
dvc stage add -n preprocess \
    -p preprocess \
    -d raw_data.csv \
    -d src/preprocess.py \
    -o processed_data.csv \
    python src/preprocess.py
```

Esto añade a `dvc.yaml`:

```yaml
stages:
  preprocess:
    cmd: python src/preprocess.py
    deps:
      - raw_data.csv
      - src/preprocess.py
    params:
      - preprocess
    outs:
      - processed_data.csv
```

**Ejemplo: etapa de entrenamiento y evaluación** (usando la salida de preprocesamiento)
```bash
dvc stage add -n train_and_evaluate \
    -p train_and_evaluate \
    -d processed_data.csv \
    -d src/train.py \
    -d src/evaluate.py \
    -o model.pkl \
    -o metrics.json \
    -o plots.png \
    python src/train.py
```

Nótese que `processed_data.csv` es una dependencia (producida por la etapa anterior). DVC infiere automáticamente el grafo acíclico dirigido (DAG).

### 2.3. Sobrescribir etapas existentes

Si se ejecuta `dvc stage add` para una etapa que ya existe, DVC mostrará un error:
```
ERROR: Stage 'train_and_evaluate' already exists in 'dvc.yaml'. Use '--force' to overwrite.
```

Para sobrescribir, usar `--force`:

```bash
dvc stage add --force -n train_and_evaluate ...
```

### 2.4. Visualización del pipeline

DVC ofrece varios comandos para visualizar el grafo de dependencias.

- **`dvc dag`**: muestra el DAG en formato texto en la terminal.
  ```bash
  dvc dag
  ```
  Salida:
  ```
  preprocess
  train_and_evaluate
  preprocess -> train_and_evaluate
  ```

- **`dvc dag --outs`**: incluye las salidas como nodos en el gráfico.
- **`dvc dag --dot`**: genera una representación en formato DOT (útil para herramientas externas).
  ```bash
  dvc dag --dot
  ```
  Produce algo como:
  ```
  strict digraph {
    "preprocess";
    "train_and_evaluate";
    "preprocess" -> "train_and_evaluate";
  }
  ```

---

## 3. Ejecución de Pipelines: `dvc repro`

### 3.1. Reproducir el pipeline

El comando `dvc repro` ejecuta las etapas del pipeline que tienen cambios en sus dependencias o parámetros, respetando el orden del DAG.

```bash
dvc repro
```

**Salida típica:**
```
Running stage 'preprocess':
> python src/preprocess.py
Running stage 'train_and_evaluate':
> python src/train.py
Updating lock file 'dvc.lock'
```

### 3.2. El archivo `dvc.lock`

Después de la primera ejecución, DVC genera un archivo `dvc.lock` que captura los hashes (MD5) de todas las dependencias y parámetros utilizados. Esto permite:
- Saber exactamente qué versiones de datos y código produjeron cada salida.
- Acelerar ejecuciones posteriores: si nada cambió, DVC omite la etapa.

```bash
# dvc.lock se debe versionar con Git
git add dvc.lock && git commit -m "Primera ejecución del pipeline"
```

### 3.3. Uso de caché para acelerar iteraciones

Si no hay cambios en las dependencias de una etapa, DVC la omite y utiliza los resultados cacheados:

```
Stage 'preprocess' didn't change, skipping
Running stage 'train_and_evaluate' with command: ...
```

Esto es fundamental para flujos de trabajo iterativos: se puede modificar solo una etapa y DVC re-ejecuta solo lo necesario.

### 3.4. Opciones útiles de `dvc repro`

- **`--dry`**: muestra qué comandos se ejecutarían, sin realmente hacerlo.
  ```bash
  dvc repro --dry
  ```
- **`-f` o `--force`**: fuerza la ejecución de todas las etapas, ignorando la caché.
- **`--no-commit`**: ejecuta pero no guarda las salidas en el caché (útil para pruebas; luego se puede hacer `dvc commit`).
- **`<target>`**: ejecuta solo una etapa específica y sus dependencias upstream.
  ```bash
  dvc repro train_and_evaluate
  ```

### 3.5. Ejecución paralela

En pipelines con ramas independientes, DVC puede ejecutar etapas en paralelo. Por ejemplo, si se tienen dos etapas de preprocesamiento independientes (`A1` y `B1`) que alimentan a una etapa común `train`, al ejecutar `dvc repro train` se ejecutarán `A1` y `B1` concurrentemente si es posible.

---

## 4. Métricas y Gráficos en DVC

### 4.1. Configuración de métricas en `dvc.yaml`

Para que DVC trate ciertos archivos como métricas (y no como salidas ordinarias), se usa la clave `metrics` en lugar de `outs`. Esto permite comparar valores entre experimentos.

**Antes (como salida normal):**
```yaml
stages:
  train_and_evaluate:
    outs:
      - metrics.json
      - plots.png
```

**Después (como métricas):**
```yaml
stages:
  train_and_evaluate:
    outs:
      - plots.png
    metrics:
      - metrics.json:
          cache: false   # opcional: no almacenar en caché (si es pequeño)
```

- Las métricas suelen ser archivos JSON, YAML o CSV con valores escalares.
- Los plots pueden ser imágenes (PNG, etc.) o archivos de datos para generar gráficos.

### 4.2. Mostrar métricas

```bash
dvc metrics show
```

Salida típica:
```
Path          accuracy  f1_score  precision  recall
metrics.json  0.947     0.8656    0.988      0.7702
```

### 4.3. Comparar métricas entre experimentos

Después de cambiar un parámetro y re-ejecutar el pipeline, se puede comparar con la versión anterior (por ejemplo, contra el último commit).

```bash
dvc metrics diff
```

Salida:
```
Path          Metric     HEAD    workspace  Change
metrics.json  accuracy   0.947   0.9995     +0.0525
metrics.json  f1_score   0.8656  0.9989     +0.1333
metrics.json  precision  0.988   0.9993     +0.0113
metrics.json  recall     0.7702  0.9986     +0.2284
```

### 4.4. Visualización de gráficos (plots)

DVC puede generar visualizaciones interactivas a partir de archivos de datos (por ejemplo, CSV con predicciones) o imágenes.

- **`dvc plots show <archivo>`**: genera un archivo HTML con el gráfico.
  ```bash
  dvc plots show predictions.csv
  ```
  Abre un archivo HTML interactivo en el navegador.

- **`dvc plots diff --target <archivo>`**: compara gráficos entre versiones (por ejemplo, contra otra rama o commit).
  ```bash
  dvc plots diff --target predictions.csv main
  ```

Esto es especialmente útil para visualizar matrices de confusión, curvas ROC, distribuciones, etc., y ver cómo cambian con diferentes versiones del modelo.

---

## 5. Resumen del Capítulo

| Comando | Descripción |
| :--- | :--- |
| `dvc stage add -n <nombre> ...` | Añade una etapa al pipeline (genera entrada en `dvc.yaml`) |
| `dvc dag` | Muestra el grafo de dependencias |
| `dvc repro` | Ejecuta el pipeline (solo etapas con cambios) |
| `dvc repro --dry` | Muestra qué se ejecutaría sin hacerlo |
| `dvc repro -f` | Fuerza re-ejecución de todas las etapas |
| `dvc repro <target>` | Ejecuta una etapa específica y sus dependencias |
| `dvc metrics show` | Muestra las métricas actuales |
| `dvc metrics diff` | Compara métricas con la versión anterior (u otra referencia) |
| `dvc plots show <archivo>` | Genera un gráfico interactivo |
| `dvc plots diff --target <archivo>` | Compara gráficos entre versiones |

**Archivos clave generados:**
- `dvc.yaml`: definición del pipeline (versionado con Git).
- `dvc.lock`: estado concreto de las ejecuciones (versionado con Git).
- `params.yaml`: parámetros centralizados (versionado con Git).

---

## 6. Buenas Prácticas

1. **Centralizar parámetros**: usar `params.yaml` y referenciarlos en `dvc.yaml`.
2. **Modularizar el código**: dividir en funciones reutilizables y testables.
3. **Versionar todo**: código, `dvc.yaml`, `dvc.lock`, `params.yaml` con Git; datos con DVC.
4. **Usar métricas y plots**: configurarlos en `dvc.yaml` para facilitar la comparación de experimentos.
5. **Aprovechar el caché**: DVC acelera iteraciones al reutilizar resultados de etapas sin cambios.
6. **Documentar el DAG**: `dvc dag` ayuda a entender el flujo y las dependencias.
