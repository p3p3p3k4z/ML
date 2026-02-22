# Apuntes de Introducción al Versionado de Datos con DVC

## 1. Motivación: ¿Por qué versionar datos?

### 1.1. ¿Qué es el versionado de datos?

El **versionado de datos** es el proceso de monitorear y gestionar los cambios en los conjuntos de datos a lo largo del tiempo, creando "instantáneas" (snapshots) en diferentes iteraciones. Es análogo al versionado de código, pero aplicado a datos.

**Beneficios clave:**
- **Recuperación y análisis:** Permite volver a versiones anteriores de los datos para auditoría o depuración.
- **Consistencia:** Asegura que todos los miembros del equipo trabajen con los mismos datos.
- **Responsabilidad (accountability):** Proporciona un historial de quién cambió qué y cuándo.
- **Linaje de datos (data lineage):** Traza el origen y las transformaciones de los datos.

**Aplicaciones:**
- Ciencia de datos y Machine Learning.
- Ingeniería de datos.
- Análisis financiero, auditoría y cumplimiento normativo.

### 1.2. Data Versioning vs. Code Versioning

| Característica | Code Versioning (Git) | Data Versioning (DVC) |
| :--- | :--- | :--- |
| **Madurez** | Bien establecido en desarrollo de software | Relativamente nuevo (SciDB propuesto en 2012) |
| **Herramientas** | Git (u otros VCS) | DVC (u otras herramientas) usadas junto con Git |
| **Tamaño** | Código fuente pequeño, fácil de gestionar | Datos grandes, difíciles de manejar con Git |
| **Almacenamiento** | Repositorios Git | Almacenamiento remoto (S3, GCS, etc.) + metadatos en Git |

### 1.3. ¿Por qué es crítico en Machine Learning?

En ML, los datos son tan importantes como el código. Cambios en los datos pueden afectar drásticamente el rendimiento del modelo.

**Ejemplo 1: Mismo modelo, diferentes datasets**

Se entrena el mismo modelo (mismos hiperparámetros) con dos datasets diferentes (A y B). Las métricas cambian significativamente:

| Métrica | Dataset A | Dataset B |
| :--- | :--- | :--- |
| Precisión | 0.78 | 0.79 |
| Recall | 0.54 | 0.57 |
| F1-Score | 0.64 | 0.66 |
| Accuracy | 0.80 | 0.81 |

**Ejemplo 2: Mismo dataset, diferentes hiperparámetros**

Se mantiene el dataset constante y se varían los hiperparámetros (ej. `n_estimators` en un Random Forest). Las métricas también cambian:

| Métrica | n_estimators=5 | n_estimators=10 |
| :--- | :--- | :--- |
| Precisión | 0.78 | 0.85 |
| Recall | 0.54 | 0.52 |
| F1-Score | 0.64 | 0.65 |
| Accuracy | 0.80 | 0.81 |

**Conclusión:** Sin versionado de datos, es imposible saber si una mejora en el modelo se debe a un mejor código/hiperparámetros o a un cambio en los datos. El versionado de datos proporciona trazabilidad y reproducibilidad.

---

## 2. Introducción a DVC (Data Version Control)

### 2.1. Git como base

**Git** es un sistema de control de versiones de código:
- Permite desarrollo local independiente mediante ramas (branch) y fusiones (merge).
- Gestiona el historial de versiones.
- Habilita la colaboración entre equipos.
- Interacción por línea de comandos (CLI).
- Guarda el contenido en un repositorio: archivos/carpetas reales + metadatos en la carpeta `.git`.

### 2.2. ¿Qué es DVC?

**DVC (Data Version Control)** es una herramienta de código abierto diseñada específicamente para gestionar el versionado de datos y experimentos en proyectos de Machine Learning.

- **Funciona junto con Git**, no lo reemplaza.
- **Git se encarga del código** y de los **metadatos** de los datos (archivos pequeños `.dvc` que apuntan a los datos).
- **DVC se encarga de los datos** en sí mismos, almacenándolos en un **almacenamiento remoto** (S3, GCS, Azure Blob, etc.) y gestionando sus versiones.

**Analogía:** DVC es para los datos lo que Git es para el código.

### 2.3. Comparativa de comandos: Git vs DVC CLI

| Acción | Git | DVC |
| :--- | :--- | :--- |
| **Inicializar repositorio** | `git init` | `dvc init` |
| **Añadir archivos (staging)** | `git add archivo.py` | `dvc add data/mi_dataset.csv` |
| **Guardar cambios (commit)** | `git commit -m "mensaje"` | `dvc commit` (guarda los datos) + `git commit` (guarda los metadatos `.dvc`) |
| **Enviar a remoto** | `git push` | `dvc push` (sube los datos al almacenamiento remoto) |
| **Recibir de remoto** | `git pull` | `dvc pull` (descarga los datos desde el almacenamiento remoto) |
| **Clonar/descargar** | `git clone https://...` | `dvc get https://... archivo.pkl` (descarga un archivo específico) |

**Flujo de trabajo típico:**
1. `git init` y `dvc init` para inicializar ambos.
2. `dvc add data/raw.csv` → crea `data/raw.csv.dvc` (metadato) y añade `raw.csv` al `.gitignore`.
3. `git add data/raw.csv.dvc` y `git commit -m "versión 1 de datos"`.
4. `dvc push` para subir los datos al remote de DVC.
5. (Otro usuario) `git pull` para obtener los metadatos y `dvc pull` para obtener los datos.

---

## 3. Características y Casos de Uso de DVC

### 3.1. Temas cubiertos en este curso

- **Versionado de datos y modelos:** El núcleo de DVC.
- **Pipelines de DVC:** Definir y ejecutar pipelines de ML reproducibles.
- **Seguimiento de métricas y gráficos:** Registrar y comparar resultados de experimentos.

### 3.2. Temas avanzados (no cubiertos)

- **Experiment tracking:** Gestión avanzada de experimentos con `dvc exp`.
- **CI/CD para Machine Learning:** Integración con pipelines de CI/CD.
- **Data registry:** Uso de DVC como un registro centralizado de datasets y modelos.

### 3.3. Pipelines en DVC (`dvc.yaml`)

DVC permite definir pipelines de procesamiento de datos y entrenamiento en un archivo `dvc.yaml`.

**Estructura básica de `dvc.yaml`:**

```yaml
stages:
  train:
    cmd: python train.py
    deps:
      - code/train.py
      - data/input_data.csv
      - params/params.json
    outs:
      - model_output/model.pkl
```

- **`cmd`**: Comando a ejecutar.
- **`deps`**: Dependencias (código, datos, parámetros). Si alguna cambia, la etapa se re-ejecuta.
- **`outs`**: Salidas (modelos, datos procesados).

Para ejecutar el pipeline:
```bash
dvc repro
```

### 3.4. Seguimiento de métricas y gráficos

DVC puede extraer métricas de archivos (ej. JSON, YAML) y mostrarlas para comparar experimentos.

```bash
dvc metrics diff
```

**Ejemplo de salida:**
```
Path          Metric    HEAD    workspace    Change
metrics.json  AUC       0.789   0.181        -0.608
metrics.json  TP        2157    68553        +66396
```

También soporta gráficos (plots) para visualizar cambios.

### 3.5. Experiment tracking (breve introducción)

DVC tiene un sistema de experimentos que permite:
- Ejecutar experimentos sin ensuciar el historial de Git.
- Guardar y comparar resultados.

**Comandos útiles:**
- `dvc exp run`: Ejecuta un experimento (combina `dvc repro` y guardado automático).
- `dvc exp save`: Guarda explícitamente un experimento.
- `dvc exp show`: Muestra una tabla comparativa de experimentos.

Los experimentos se almacenan como referencias personalizadas de Git, sin crear commits masivos.

### 3.6. Data Registry

DVC puede usarse para crear un **registro centralizado de datos y modelos**, similar a un "GitHub para datos". Permite:
- Publicar versiones estables de datasets.
- Compartir modelos entrenados.
- Gestionar accesos y versiones.

---

## 4. Resumen y flujo de trabajo recomendado

### 4.1. Flujo básico con DVC y Git

```bash
# 1. Inicializar repositorios
git init
dvc init

# 2. Añadir datos a DVC
dvc add data/raw_dataset.csv

# 3. Añadir metadatos a Git
git add data/raw_dataset.csv.dvc .gitignore
git commit -m "Añadir dataset versión 1"

# 4. Configurar almacenamiento remoto (ej. S3)
dvc remote add -d myremote s3://mybucket/dvcstore

# 5. Subir datos al remoto
dvc push

# 6. (En otra máquina) Clonar código y descargar datos
git clone https://github.com/user/project.git
cd project
dvc pull
```

### 4.2. Beneficios clave de DVC

- **Reproducibilidad:** Saber exactamente qué datos y código generaron un modelo.
- **Colaboración:** Todos los miembros del equipo trabajan con los mismos datos.
- **Trazabilidad:** Historial completo de cambios en datos y modelos.
- **Eficiencia:** No se duplican datos enormes; DVC maneja las diferencias.
- **Integración con Git:** Aprovecha toda la potencia de Git para el código.

---

## 5. Cheat Sheet de comandos DVC

| Comando | Descripción |
| :--- | :--- |
| `dvc init` | Inicializa DVC en el proyecto actual |
| `dvc add archivo` | Comienza a versionar un archivo/directorio de datos |
| `dvc commit` | Guarda los cambios de los datos versionados |
| `dvc push` | Sube datos al almacenamiento remoto |
| `dvc pull` | Descarga datos desde el almacenamiento remoto |
| `dvc get URL archivo` | Descarga un archivo específico de un repositorio DVC |
| `dvc repro` | Ejecuta el pipeline definido en `dvc.yaml` |
| `dvc metrics diff` | Muestra diferencias en métricas entre versiones |
| `dvc exp run` | Ejecuta un experimento |
| `dvc exp show` | Muestra la tabla de experimentos |
| `dvc remote add nombre URL` | Configura un almacenamiento remoto |

---

## Conclusión

DVC es la herramienta fundamental para llevar las buenas prácticas de versionado (heredadas de Git) al mundo de los datos y el Machine Learning. Permite rastrear, compartir y reproducir experimentos con total confianza, resolviendo el problema de "¿este modelo mejoró por el código o por los datos?". Los siguientes capítulos profundizarán en pipelines, métricas y experimentos.