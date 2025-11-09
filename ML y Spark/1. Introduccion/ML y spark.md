## Machine Learning con Apache Spark 🧠

El objetivo es **construir modelos de aprendizaje automático** (ML) con conjuntos de datos masivos (Big Data) **utilizando técnicas de computación distribuida**.

### El Problema: El "Hotcake Perfecto" a Gran Escala 🥞

Podemos pensar en el ML como un proceso para encontrar la "receta del hotcake perfecto".

1.  **Enfoque Tradicional:** Le presentamos a la computadora una receta y aprende de ella.
2.  **Enfoque ML:** Le presentamos una **selección de miles o millones de recetas** (los datos), y el modelo **descubrirá los mejores ingredientes y proporciones** (los parámetros) para predecir el mejor resultado (ej. la calificación del hotcake).

#### ¿Cómo Funciona el Aprendizaje Automático?

La computadora **aprende de ejemplos**. En el aprendizaje supervisado (el más común), esto se divide en:

* **Regresión:** Predecir un valor que **generalmente es numérico** y continuo.
    * *Ejemplo:* ¿**Cuánta harina** se deberá poner para un hotcake de 10 cm?
* **Clasificación:** Predecir un **valor discreto o categórico** (una etiqueta).
    * *Ejemplo:* ¿Este ingrediente es "sal" o es "azúcar"?

---

### El Límite de una Sola Máquina: El Cuello de Botella

Cuando el conjunto de datos es pequeño, **si los datos caben en la memoria RAM** de una computadora, el procesamiento es rápido.

* **El Problema:** Cuando el conjunto de datos es masivo (Big Data), no cabe en la RAM. El sistema operativo utiliza la **memoria virtual** (espacio en el disco duro) y los **datos se "paginarán"** (se mueven constantemente entre el disco y la RAM).
* **La Consecuencia:** Esto hace que **el rendimiento se desplome**, ya que el acceso al disco es miles de veces más lento que el acceso a la RAM.

La solución es **distribuir el procesamiento** en múltiples máquinas, y **este es el enfoque de Spark**.

---

### Apache Spark: La Solución Distribuida 🚀

Spark es un **marco (framework) de propósito general para la computación en clúster**.

* **Velocidad:** Es mucho **más rápido que marcos tradicionales** de Big Data (como el MapReduce de Hadoop), porque **realiza la mayor parte del procesamiento en memoria (in-memory)** a través de los diferentes nodos del clúster.
* **Interfaz Amigable:** Provee una API de alto nivel (en Scala, Python, R, SQL) que **oculta la complejidad de la computación distribuida**.
* **Spark MLlib:** Es la biblioteca específica de Spark diseñada para realizar Machine Learning de forma distribuida, aprovechando toda la arquitectura del clúster.

---

### 🏗️ Arquitectura Básica de Spark

Spark funciona coordinando un conjunto de computadoras (un clúster).

* **Clúster:** Consta de varios **Nodos** (Workers). Cada nodo es una computadora individual con su propia CPU, RAM y almacenamiento físico.
* **Componentes Clave:**
    * **Administrador de Clúster (Cluster Manager):** Es el software que **asigna los recursos** de hardware a las aplicaciones (ej. YARN, Mesos o el propio de Spark).
    * **Programa Controlador (Driver):** Cada aplicación que se ejecuta en el clúster (ej. tu script de ML) tiene un **programa controlador** (es el `main()` de tu app).
    * **Ejecutor (Executor):** Es un proceso que Spark lanza en cada nodo. Este proceso **persiste mientras dura la aplicación** y es el que realmente hace el trabajo.

#### Flujo de Funcionamiento

1.  Al utilizar la API de Spark, el **Controlador (Driver)** se comunica con el **Administrador del Clúster**.
2.  El Administrador, a su vez, **distribuye el trabajo** a los nodos disponibles, asignando **Ejecutores** para la aplicación.
3.  El trabajo se divide en **Tareas (Tasks)**, que son las unidades mínimas de cálculo (ej. procesar una partición de los datos).
4.  Los **Ejecutores** en cada nodo ejecutan estas tareas, a menudo usando múltiples **subprocesos (threads)** en los diferentes núcleos (cores) del nodo para lograr el paralelismo.