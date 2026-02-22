# 📑 Reporte Técnico: Orquestación de ML con DVC

**Asunto:** Gestión de Ciclo de Vida de Datos y Modelos (MLOps)

**Tecnologías:** DVC (Data Version Control), Git, YAML, Python.

---

## 🏛️ 1. Arquitectura del Proyecto

El flujo de trabajo se divide en tres capas de control:

1. **Código (`.py`)**: Lógica de procesamiento y entrenamiento.
    
2. **Parámetros (`params.yaml`)**: Variables de configuración (hiperparámetros).
    
3. **Pipeline (`dvc.yaml`)**: Definición del Grafo Acíclico Dirigido (DAG) que conecta todo.
    

---

## ⚙️ 2. Configuración de Parámetros (`params.yaml`)

Este archivo centraliza las decisiones del proyecto. Si cambias un valor aquí, DVC detectará qué etapas del pipeline deben re-ejecutarse.

YAML

```
preprocess:
  drop_colnames:
    - Date
  target_column: RainTomorrow

train_and_evaluate:
  test_size: 0.2
  rfc_params:
    n_estimators: 3
    max_depth: 2
    random_state: 42
```

---

## 🔗 3. Definición del Pipeline (`dvc.yaml`)

Es el orquestador. Aquí se definen las **dependencias (`deps`)**, las **salidas (`outs`)** y las **métricas/gráficas**.

YAML

```
stages:
  preprocess_stage:
    cmd: python3 preprocess.py
    deps:
      - raw_data.csv
      - preprocess.py
    params:
      - preprocess
    outs:
      - processed_data.csv

  train_stage:
    cmd: python3 train.py
    deps:
      - processed_data.csv
      - train.py
    params:
      - train_and_evaluate
    outs:
      - model.pkl

  evaluate_stage:
    cmd: python3 evaluate.py
    deps:
      - model.pkl
      - eval_data.csv
    metrics:
      - metrics.json:
          cache: false
    plots:
      - predictions.csv:
          template: confusion
          x: actual
          y: predicted
          cache: false
```

---

## 🛠️ 4. Guía de Comandos Esenciales (Workflow)

### A. Gestión de Versiones y Datos

- `dvc init`: Inicializa el proyecto.
    
- `dvc add data.csv`: Empieza a rastrear un archivo pesado (genera `data.csv.dvc`).
    
- `git reset --hard HEAD~1` + `dvc checkout`: **El "Botón de Pánico"**. Revierte el código en Git y sincroniza los datos pesados automáticamente para que coincidan.
    

### B. Ejecución y Reproducibilidad

- `dvc repro`: El comando maestro. Ejecuta solo las etapas que cambiaron.
    
- `dvc dag`: Muestra visualmente en la terminal cómo están conectadas tus etapas.
    

### C. Análisis de Resultados

- `dvc metrics show`: Despliega el rendimiento actual (ej. Accuracy, F1-Score).
    
- `dvc metrics diff`: Compara el rendimiento actual contra el último commit de Git. **Fundamental para saber si tu cambio en `n_estimators` sirvió de algo.**
    
- `dvc plots show`: Genera el archivo `index.html` con las gráficas interactivas.
    

---

## 🏛️ Análisis de Ingeniería: El valor para un SysAdmin/DevOps

1. **Optimización de Cómputo:** Gracias al almacenamiento en caché, si solo cambias la etapa de evaluación, no pierdes tiempo re-entrenando el modelo. En tu equipo con **4GB de RAM**, esto evita saturar el swap innecesariamente.
    
2. **Integridad:** El archivo `dvc.lock` asegura que si compartes el proyecto con un compañero de la **UTM**, él obtendrá **exactamente** los mismos resultados que tú.
    
3. **Separación de Responsabilidades:** Git guarda el "quién y cuándo" del código; DVC guarda el "qué" de los datos masivos.
    
