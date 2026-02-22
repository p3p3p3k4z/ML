
### 1. Inspeccionar el historial de Git

Para ver los cambios que se han registrado en el repositorio (incluyendo los cambios en los archivos `.dvc`):

Bash

```
git log
```

_(Recuerda pulsar **q** para salir del log)._

---

### 2. Comparar el Hash (Integridad de datos)

DVC utiliza el hash MD5 para saber si un archivo ha cambiado. Vamos a comparar el valor esperado por DVC contra el archivo real en el disco:

Bash

```
# Ver el hash guardado en los metadatos de DVC
cat dataset.csv.dvc

# Calcular el hash real del archivo actual
md5sum dataset.csv
```

---

### 3. Revertir el commit de Git (Rollback de metadatos)

Queremos volver al estado anterior. Al hacer esto, el archivo `dataset.csv.dvc` volverá a su versión antigua (la que tenía antes de borrar las 1000 líneas), pero el archivo `dataset.csv` seguirá siendo el "nuevo" (el corto).

Bash

```
git reset --hard HEAD~1
```

> **Nota de Ingeniería:** En este punto tienes una **inconsistencia**. Los metadatos de Git dicen que el archivo debería tener un MD5, pero en tu espacio de trabajo tienes el archivo modificado. Si corres `md5sum dataset.csv` ahora, verás que no coincide con el nuevo `dataset.csv.dvc`.

---

### 4. Sincronizar los datos con DVC (Checkout)

Para resolver la inconsistencia y recuperar las 1000 líneas borradas, le pedimos a DVC que "traiga" la versión del archivo que coincide con los metadatos actuales de Git:

Bash

```
dvc checkout
```

---

### 🏛️ Análisis de Ingeniería: El flujo Git + DVC

Desde tu perspectiva de **SysAdmin**, este flujo es como gestionar instantáneas (snapshots) de un sistema de archivos:

1. **Git reset**: Cambia el "puntero" del historial. Es rápido porque solo mueve texto pequeño (los metadatos `.dvc`).
    
2. **DVC checkout**: Es el comando que realmente mueve los bits pesados desde el cache de DVC (`.dvc/cache`) hacia tu directorio de trabajo.
    
3. **Consistencia**: Siempre que cambies de rama o hagas un reset en Git, debes ejecutar `dvc checkout` para que tus archivos de datos (CSV, modelos de IA, etc.) se sincronicen con la versión del código.
    
