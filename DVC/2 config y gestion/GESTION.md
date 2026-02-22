# Apuntes de DVC: Configuración, Inicialización y Gestión de Datos

## 1. Instalación y Configuración Inicial

### 1.1. Instalación de DVC

DVC es un paquete de Python que se instala fácilmente con `pip`. Se recomienda hacerlo dentro de un entorno virtual para evitar conflictos con otras dependencias.

```bash
pip install dvc
```

**Requisito previo:** Git debe estar instalado en el sistema, ya que DVC se integra estrechamente con él.

### 1.2. Verificación de la instalación

Para confirmar que DVC se instaló correctamente y ver la versión, información de la plataforma, etc.:

```bash
dvc version
```

Este comando muestra detalles como la versión de DVC, el intérprete de Python, la plataforma y la versión de Git.

### 1.3. Inicialización de un repositorio DVC

DVC debe inicializarse dentro de un repositorio Git existente. El proceso crea la estructura interna necesaria.

```bash
# Asegurarse de estar en un repositorio Git (o iniciarlo primero)
git init
dvc init
```

Después de `dvc init`, se generan los siguientes archivos/carpetas:

- `.dvc/`: directorio interno de DVC (contiene configuración, caché, etc.).
- `.dvc/.gitignore`: asegura que ciertos archivos internos no sean trackeados por Git.
- `.dvc/config`: archivo de configuración de DVC.
- `.dvcignore`: similar a `.gitignore`, pero para DVC (especifica archivos que DVC debe ignorar).

Estos archivos deben ser versionados con Git:

```bash
git status
# Se verán los nuevos archivos listos para commit
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

### 1.4. El archivo `.dvcignore`

`.dvcignore` permite excluir archivos o patrones del seguimiento de DVC. Su sintaxis es idéntica a la de `.gitignore`. Es útil para ignorar archivos temporales, cachés locales o cualquier otro que no deba ser parte del versionado de datos.

**Verificar si un archivo está ignorado:**

```bash
dvc check-ignore <nombre_archivo>
```

Este comando indica si el archivo especificado está siendo excluido por alguna regla en `.dvcignore`.

---

## 2. Caché y Archivos de Staging en DVC

### 2.1. El caché de DVC

El **caché** es un área de almacenamiento oculta (dentro de `.dvc/cache`) donde DVC guarda copias de los datos versionados. Funciona como un "staging area" para archivos grandes antes de ser confirmados.

- Por defecto, el caché reside en `.dvc/cache` dentro del proyecto.
- Se puede cambiar su ubicación con:

```bash
dvc cache dir /ruta/deseada
```

**Importante:** El caché contiene los datos reales, organizados por su hash MD5. Esto permite deduplicación y eficiencia.

### 2.2. Añadir archivos al caché (`dvc add`)

Para comenzar a versionar un archivo de datos con DVC:

```bash
dvc add data.csv
```

Este comando:
1. Calcula el hash MD5 del archivo.
2. Copia el archivo al caché (en `.dvc/cache` con subdirectorios basados en el hash).
3. Crea un archivo `.dvc` con metadatos (ver sección 2.3).
4. Añade el archivo original al `.gitignore` (para que Git no lo trackee directamente).
5. Muestra instrucciones para continuar con Git.

Salida típica:
```
100% Adding...|=============|1/1 [00:00, 53.55file/s]
To track the changes with git, run:
    git add data.csv.dvc
To enable auto staging, run:
    dvc config core.autostage true
```

### 2.3. Archivos `.dvc`: metadatos de los datos

Por cada archivo o directorio añadido con `dvc add`, se genera un archivo `.dvc` (ej. `data.csv.dvc`). Este archivo contiene metadatos que permiten a DVC saber qué versión de los datos está asociada.

**Contenido típico de un `.dvc`:**

```yaml
outs:
  - md5: f38a850818377e97155d22755caa39d0
    size: 16
    hash: md5
    path: data.csv
```

- **`md5`**: hash del contenido del archivo. DVC usa este hash para localizar el archivo en el caché.
- **`path`**: ruta relativa al archivo original.

Estos archivos `.dvc` son pequeños y deben ser versionados con Git (no los datos en sí). Así, Git maneja los metadatos y DVC maneja los datos pesados.

### 2.4. Relación entre caché y archivos `.dvc`

La ruta de un archivo en el caché se construye a partir de su hash MD5. Por ejemplo, si el hash es `f38a850818377e97155d22755caa39d0`, el archivo estará en:

```
.dvc/cache/f3/8a850818377e97155d22755caa39d0
```

(Se toman los dos primeros caracteres como subdirectorio para evitar problemas con sistemas de archivos que tienen límites en el número de archivos por directorio.)

**Verificación:** Podemos calcular el MD5 del archivo original y comparar:

```bash
md5 data.csv
# MD5 (data.csv) = f38a850818377e97155d22755caa39d0
```

Coincide con el nombre en caché.

### 2.5. Eliminar archivos del caché y limpieza

- **`dvc remove <archivo.dvc>`**: Elimina el archivo `.dvc` y también la entrada correspondiente del caché (si no es referenciada por otro archivo).
- **`dvc gc`**: Garbage collector. Limpia el caché eliminando archivos que no están siendo usados por ninguna versión en el workspace o en el historial de Git. La opción `-w` limita la limpieza al workspace actual.

```bash
dvc gc -w
```

Advertencia: preguntará confirmación antes de eliminar.

---

## 3. Configuración de Remotos (DVC Remotes)

### 3.1. ¿Por qué necesitamos remotos?

Los **remotos** en DVC son análogos a los remotos de Git, pero para almacenar los datos versionados (el contenido del caché). Permiten:

- Compartir datos y modelos con el equipo.
- Sincronizar archivos grandes entre máquinas.
- Centralizar el almacenamiento (en la nube o en un servidor local).
- Ahorrar espacio local (se puede descargar solo lo necesario).

### 3.2. Tipos de almacenamiento soportados

DVC soporta una amplia variedad de remotos:

- **Almacenamiento en la nube**: Amazon S3, Google Cloud Storage, Azure Blob Storage, etc.
- **Servidores remotos vía SSH**, HDFS, HTTP.
- **Almacenamiento local** (otro directorio en el mismo sistema o en un NAS).

### 3.3. Añadir un remoto

El comando básico es:

```bash
dvc remote add <nombre> <ubicación>
```

Ejemplos:

```bash
# Remoto S3
dvc remote add s3_remote s3://mi-bucket/dvc-store

# Remoto GCP
dvc remote add gcp_remote gs://mi-bucket/dvc-store

# Remoto Azure
dvc remote add azure_remote azure://micontenedor/ruta

# Remoto local (para pruebas)
dvc remote add local_remote /tmp/dvc-remoto
```

Esto agrega una entrada en `.dvc/config`:

```
['remote "s3_remote"']
    url = s3://mi-bucket/dvc-store
```

### 3.4. Establecer un remoto por defecto

Con la opción `-d` se indica que este remoto será el predeterminado para operaciones como `dvc push` y `dvc pull`.

```bash
dvc remote add -d default_remote /tmp/dvc-remoto
```

Esto añade en la sección `[core]` del archivo de configuración:

```
[core]
    remote = default_remote
```

### 3.5. Listar remotos configurados

```bash
dvc remote list
```

Muestra todos los remotos con sus URLs.

### 3.6. Modificar propiedades de un remoto

Para ajustar parámetros específicos de un remoto (por ejemplo, tiempo de espera, región, credenciales), se usa:

```bash
dvc remote modify <nombre> <propiedad> <valor>
```

Ejemplo:

```bash
dvc remote modify s3_remote connect_timeout 300
```

Esto añade la línea `connect_timeout = 300` en la sección del remoto en la configuración.

---

## 4. Interacción con Remotos: Push, Pull, Fetch

### 4.1. Subir datos al remoto (`dvc push`)

Una vez que tenemos datos en el caché local y queremos compartirlos o respaldarlos, usamos:

```bash
dvc push [<target>...]
```

- Sin argumentos: sube todos los datos del caché que no estén ya en el remoto.
- Con un target específico (ej. `data.csv`): sube solo ese archivo.

Opciones útiles:
- `-r <remote>`: especificar un remoto diferente al predeterminado.
- `-v`: modo verbose para depuración.

### 4.2. Descargar datos del remoto (`dvc pull`)

Para obtener los datos desde el remoto y restaurarlos en el workspace:

```bash
dvc pull [<target>...]
```

Similar a `git pull`, pero para datos. Descarga los archivos necesarios según los archivos `.dvc` presentes.

### 4.3. Actualizar el caché sin modificar el workspace (`dvc fetch`)

A veces solo se quiere descargar los datos al caché sin que aparezcan aún en el workspace (por ejemplo, para prepararse antes de un checkout). Esto se hace con:

```bash
dvc fetch [<target>...]
```

Luego, un `dvc checkout` restauraría los datos al workspace.

### 4.4. Comparación con Git

| Acción | Git | DVC |
| :--- | :--- | :--- |
| Subir cambios | `git push` | `dvc push` |
| Bajar cambios | `git pull` | `dvc pull` |
| Descargar metadatos/datos | `git fetch` | `dvc fetch` |
| Almacenamiento remoto | Repositorio Git | Almacenamiento de objetos (S3, etc.) |

---

## 5. Versionado de Datos con DVC y Git

### 5.1. El flujo completo de versionado

1. **Añadir datos** con `dvc add` → se genera el archivo `.dvc`.
2. **Versionar el `.dvc`** con Git (`git add`, `git commit`).
3. **Subir los datos** al remoto con `dvc push`.
4. **Subir los metadatos** (`.dvc`) al remoto Git con `git push`.

### 5.2. Recuperar una versión específica de los datos

Dado que los archivos `.dvc` están versionados por Git, podemos movernos a cualquier commit, tag o rama que contenga un `.dvc` antiguo y luego restaurar los datos correspondientes.

```bash
# Cambiar a un commit anterior que contiene un .dvc específico
git checkout <commit_hash> -- data.csv.dvc

# Restaurar los datos asociados a ese .dvc
dvc checkout data.csv
```

El comando `dvc checkout` lee el hash del archivo `.dvc` y recupera los datos desde el caché (o desde el remoto si es necesario).

### 5.3. Registrar cambios en los datos

Cuando un archivo de datos se modifica, el proceso para versionar la nueva versión es:

```bash
# 1. Actualizar el archivo (ej. editando data.csv)
# 2. Volver a añadirlo a DVC
dvc add data.csv

# 3. Añadir el .dvc actualizado a Git
git add data.csv.dvc
git commit -m "Actualización del dataset"

# 4. Subir los nuevos datos al remoto DVC
dvc push

# 5. Subir los metadatos a Git
git push
```

---

## 6. Resumen y Buenas Prácticas

| Comando | Descripción |
| :--- | :--- |
| `dvc init` | Inicializa DVC en el repositorio Git |
| `dvc add <archivo>` | Comienza a versionar un archivo de datos |
| `dvc remove <archivo.dvc>` | Elimina el archivo del control de DVC |
| `dvc push` | Sube datos al remoto |
| `dvc pull` | Descarga datos desde el remoto |
| `dvc fetch` | Descarga datos solo al caché |
| `dvc checkout` | Restaura datos desde el caché al workspace |
| `dvc remote add <nombre> <url>` | Configura un nuevo remoto |
| `dvc remote list` | Lista remotos configurados |
| `dvc remote modify <nombre> <prop> <valor>` | Ajusta parámetros de un remoto |
| `dvc gc -w` | Limpia el caché de archivos no usados |
| `dvc check-ignore <archivo>` | Verifica si un archivo está ignorado por `.dvcignore` |

**Flujo recomendado para un proyecto con DVC:**

1. Inicializar Git y DVC.
2. Configurar un remoto (local o en la nube) para los datos.
3. Añadir datasets, modelos o cualquier archivo grande con `dvc add`.
4. Commitear los archivos `.dvc` en Git.
5. Hacer `dvc push` para respaldar los datos.
6. Compartir el repositorio Git; los colaboradores harán `git clone` y luego `dvc pull` para obtener los datos.
7. Para nuevas versiones de datos, repetir pasos 3-5.

Con esta base, DVC se convierte en una extensión natural de Git que permite manejar proyectos de Machine Learning con trazabilidad y reproducibilidad totales.