Continuemos con nuestra inmersión en **MLOps**. Mientras que en la sesión anterior definimos el "qué" y los roles, ahora profundizaremos en la **Fase de Diseño** y el **Corazón del Desarrollo** (Ingeniería de Datos y Experimentación).

---

## I. MLOps Design: La Base Estratégica

Antes de escribir una sola línea de código, el diseño define el rumbo del proyecto. ML no es solo lanzar algoritmos; es una inversión que debe justificarse.

### 1. Valor Añadido y Expectativas

Dado que ML es inherentemente **experimental e incierto**, es vital estimar el valor esperado antes de empezar.

- **Priorización:** Ayuda a decidir qué proyectos merecen recursos.
    
- **Asignación de recursos:** Permite gestionar presupuestos y personal de forma eficiente.
    
- **Gestión de expectativas:** Evita promesas imposibles a los _stakeholders_.
    

### 2. Requisitos de Negocio

Se dividen en lo que el usuario necesita y lo que la organización puede permitir:


- **Usuario Final:** Busca velocidad, precisión y transparencia en las decisiones del modelo .
    
- **Organización:** Debe lidiar con el presupuesto, el tamaño del equipo y el cumplimiento de normativas y regulaciones.
 
### 3. Métricas Clave (Success Metrics)

El éxito se mide de forma distinta según quién mire el modelo:

- **Data Scientist:** Se enfoca en la **Accuracy** (Precisión técnica).
    
- **Subject Matter Expert:** Se enfoca en la **Felicidad del Cliente**.
    
- **Business Stakeholder:** Se enfoca en los **Ingresos generados** ($).
    

---

## II. Calidad e Ingesta de Datos (Data Engineering)

En MLOps, el modelo es tan bueno como los datos que lo alimentan. La calidad del dato mide qué tan bien sirven para su propósito.

### 1. Dimensiones de Calidad

Para verificar si tus datos son aptos, evaluamos estas dimensiones:

- **Exactitud (Accuracy):** ¿Los datos describen correctamente la realidad? (Ej: ¿La edad es 18 o 32?) .
    
- **Completitud (Completeness):** ¿Faltan datos críticos? (Ej: ¿Falta el apellido del 80% de los clientes?) .
 
- **Consistencia (Consistency):** ¿La definición de "cliente" es igual en toda la empresa?.

- **Oportunidad (Timeliness):** ¿Están los datos disponibles cuando se necesitan? (Ej: Datos en tiempo real vs. sincronización al final del día) .

### 2. Ingesta de Datos: El flujo ETL

El proceso estándar para mover datos desde fuentes externas (clima, órdenes) hacia una base de datos centralizada:

1. **Extract (Extraer):** Obtener los datos crudos.
    
2. **Transform (Transformar):** Combinar, limpiar y procesar los datos.

3. **Load (Cargar):** Almacenar el resultado en la base de datos final.

---

## III. Feature Engineering y Gestión de Versiones

Es el proceso de transformar datos crudos en variables (features) que el modelo pueda procesar eficientemente.

### 1. Herramientas de MLOps para Features

- **Feature Selection:** No todas las variables sirven. Usamos conocimientos del dominio, **correlación** e importancia de características para elegir las mejores .
    
- **Feature Store:** Un repositorio central para transformar, almacenar y servir vectores de características. Es vital en equipos grandes que reutilizan variables en múltiples proyectos.

- **Data Version Control (DVC):** Es "Git para datos". Permite rastrear cambios en los datasets y mantener la consistencia en todo el ciclo de vida.


---

## IV. El Laboratorio de ML: Seguimiento de Experimentos

Experimentar es el núcleo del desarrollo. Rastrear experimentos permite comparar resultados, reproducir pruebas pasadas y colaborar mejor .

### ¿Qué factores debemos rastrear?

Para que un experimento sea reproducible, debemos registrar:

1. **Modelos:** Qué algoritmos se usaron.
    
2. **Hiperparámetros:** Configuraciones internas del modelo.
    
3. **Versiones de datos:** Qué dataset exacto se usó (aquí entra DVC).
    
4. **Scripts de ejecución:** El código exacto ejecutado.
    
5. **Configuraciones de entorno:** Librerías, versiones de Python, etc.
    

### El Proceso Experimental (8 Pasos)

1. **Formular hipótesis:** "Esperamos que...".
    
2. **Recopilar datos y etiquetas**.
    
3. **Definir experimentos** (modelos, hiperparámetros).
    
4. **Configurar el rastreo** (Experiment tracking).
    
5. **Entrenar los modelos**.
    
6. **Probar en un conjunto de prueba retenido** (Hold-out test set).
    
7. **Registrar el modelo más adecuado**.
    
8. **Reportar y visualizar** resultados para determinar los siguientes pasos.
    

---

### 🛠️ Reflexión para tu perfil DevOps

Fíjate en el punto de **Data Version Control (DVC)** y **Rastreo de Experimentos**. En un entorno de producción, si un modelo empieza a fallar, tu labor como DevOps será hacer un "rollback" no solo del código, sino de los **datos** y el **entorno** que lo generó. Por eso herramientas como DVC y plataformas de rastreo son la columna vertebral de la estabilidad en MLOps.
