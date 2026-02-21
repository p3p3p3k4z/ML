# Apuntes de MLOps: Ejecución y Despliegue (Serving & Deployment)

## 1. Modos de Servicio (Serving Modes)

El primer paso para poner un modelo en producción es decidir **cómo** va a ser servido. Esta decisión depende fundamentalmente de los requisitos de latencia del caso de uso.

- **Model Serving:** Es el acto de proporcionar un servicio de predicción.
- **Serving Mode:** Es la implementación específica de ese servicio. ¡Elegir bien es crucial!

### 1.1. Predicción por Lotes (Batch Prediction)
- **Filosofía:** "Keep it simple".
- **Funcionamiento:** Se ejecutan predicciones sobre un conjunto de datos en lotes programados (ej. cada hora, cada día, cada mes).
- **Latencia aceptable:** Horas, días.
- **Cuándo usarlo:** Si el caso de negocio lo permite, es la opción más sencilla.
- **Ejemplo:** Generación mensual de previsiones de ventas.

### 1.2. Predicción Casi en Tiempo Real (Near-Real Time Prediction)
- **Funcionamiento:** También conocido como **procesamiento de streams (Stream Processing)** . Las solicitudes y respuestas forman "flujos de datos" continuos.
- **Latencia aceptable:** Del orden de minutos.

### 1.3. Predicción en Tiempo Real (Real-Time Prediction)
- **Filosofía:** La latencia es la prioridad máxima.
- **Latencia aceptable:** < 1 segundo.
- **Ejemplo:** Detección de fraudes con tarjetas de crédito. Una predicción tardía es tan inútil como no tener ninguna.

### 1.4. Despliegue en el Borde (Edge Deployment)
- **Contexto:** Cuando la latencia es una prioridad y la conexión a un servidor central es un cuello de botella.
- **Estrategia:** Modelos desplegados directamente en los dispositivos de los usuarios finales.
- **Compromiso:** Un modelo más débil pero rápido puede ser más valioso que uno más potente pero lento.
- **Ejemplos:**
    - Aplicaciones de navegación GPS.
    - Desbloqueo facial en smartphones.
    - Filtros de imágenes en tiempo real.

---

## 2. Construyendo la API: El Puente al Mundo Exterior

Para servir un modelo en tiempo real, necesitamos un **servidor**: una aplicación que expone nuestro modelo ML a los clientes.

### 2.1. Concepto de API
Una API permite que aplicaciones cliente (apps, webs) se comuniquen con nuestro servidor para ejecutar procedimientos, acceder a bases de datos remotas o, en nuestro caso, obtener predicciones.

- **Ejemplos del mundo real:**
    - API de análisis de sentimiento de Amazon Comprehend.
    - API de Twitter.
    - API de New York Times.

### 2.2. Visión Agnóstica de la Arquitectura
Existen varios estilos de arquitectura de APIs (REST, RPC, SOAP), pero para este curso, nos centraremos en los conceptos universales.

### 2.3. Ejemplo Práctico: App de Navegación
Imaginemos una API cuyo propósito es permitir que las apps cliente calculen el tiempo estimado de llegada (ETA).
1.  **Cliente:** La app de navegación envía datos.
2.  **API:** Recibe la solicitud, la procesa con el modelo y devuelve la predicción.

### 2.4. Validación de Entrada: La Primera Línea de Defensa
Un aspecto crítico en la API es **validar los datos que envía el cliente** antes de que lleguen al modelo.

- **Problema:** ¿Qué pasa si el cliente envía un valor no numérico para la velocidad (`velocity`) cuando el modelo espera un número?
- **Acción:** La API debe verificar que todos los atributos existen y tienen los tipos correctos.
- **Expectativas (Data Expectations):** Debemos definir y hacer cumplir las reglas.
    - `v` (velocidad) = número real positivo.
    - `d` (distancia) = número real positivo.

### 2.5. Herramienta Clave: FastAPI
- **Qué es:** Un framework de código abierto para construir APIs en Python.
- **Ventaja:** Incluye todas las características esenciales (validación, documentación automática, etc.) listas para usar, permitiendo lanzar APIs REST en muy poco tiempo.

---

## 3. Progresión del Despliegue y Tipos de Pruebas

**Regla de oro:** No te apresures a desplegar sin pruebas exhaustivas. Un solo eslabón débil puede romper todo el sistema.

> **Analogía:** El desastre del transbordador espacial Challenger en 1986 fue causado por un simple anillo de sellado de goma que falló.

### 3.1. Agenda de Pruebas (In Scope: La app ML completa, no el rendimiento del modelo)

- **Pruebas Unitarias (Unit Tests):**
    - Verificar que unidades de código independientes funcionan como se espera.
    - **Ejemplo:** Probar una función `add_two_numbers(x, y)` para asegurar que `add_two_numbers(1, 1) == 2`.
- **Pruebas de Integración (Integration Tests):**
    - Verificar que los diferentes módulos o servicios (ej. API, base de datos, modelo) funcionan correctamente juntos.
- **Pruebas de Humo (Smoke Tests):**
    - Pruebas rápidas y superficiales para verificar que la aplicación se inicia y responde, sin errores fatales.
- **Pruebas de Carga (Load Tests):**
    - Evaluar cómo se comporta el sistema bajo una carga de trabajo esperada y alta.
- **Pruebas de Aceptación (Acceptance Tests / UAT):**
    - Validar que el sistema cumple con los criterios y necesidades del negocio/usuario final.

### 3.2. Entornos de Desarrollo, Prueba y Despliegue

Es fundamental tener entornos separados para cada etapa del ciclo de vida.

1.  **Entorno de Desarrollo (Development - DEV):**
    - **Propósito:** Experimentación. Todo cambia constantemente.
    - **Características:** Código en desarrollo, bases de datos de desarrollo (ej. Dev DB X, Dev DB Y), servidores de desarrollo.

2.  **Entorno de Pruebas (Test):**
    - **Propósito:** Estable y dedicado a la ejecución de pruebas.
    - **Acción:** Aquí es donde se ejecutan las pruebas unitarias y de integración de forma fiable.
    - **Beneficio:** Libera recursos del entorno de desarrollo y proporciona un entorno consistente para la validación.

3.  **Entorno de Preproducción (Staging):**
    - **Propósito:** Espejo del entorno de producción. Aquí se realizan las pruebas de aceptación (UAT), carga y humo antes del lanzamiento final.

4.  **Entorno de Producción (Production):**
    - **Propósito:** El entorno real donde los usuarios interactúan con la aplicación.

### 3.3. No te pierdas, ¡Prioriza!
Con tantos tipos de pruebas y entornos, es fácil desviarse. El objetivo es la calidad y la seguridad, no la cantidad de pasos burocráticos.

---

## 4. Estrategias de Despliegue de Modelos

Una vez que tenemos un nuevo modelo (con mejores features, entrenado con nuevos datos), debemos decidir **cómo** reemplazar al modelo antiguo en producción sin causar interrupciones. Aunque el PDF no detalla las estrategias, las nombra como un tema crucial. Aquí tienes un resumen de las más comunes para complementar tus apuntes:

### 4.1. Estrategia "Todo o Nada"
- **Recreación (Recreate):** Se detiene la versión antigua (v1) y se despliega la nueva (v2). Es simple pero causa tiempo de inactividad.

### 4.2. Estrategias de Disponibilidad Continua
- **Despliegue Continuo (Rolling Update):** Se reemplazan las instancias de v1 con v2 de forma gradual. No hay tiempo de inactividad, pero durante la transición, conviven ambas versiones.
- **Azul/Verde (Blue/Green):** Se despliega v2 en un entorno paralelo (verde) idéntico al de producción (azul). Una vez probado, se cambia el enrutador de tráfico del azul al verde. El rollback es instantáneo.
- **Canario (Canary Deployment):** Se despliega v2 solo para un pequeño porcentaje de usuarios (los "canarios"). Se monitoriza su rendimiento y, si es bueno, se va aumentando el tráfico gradualmente hasta que reemplaza a v1. Es la estrategia más segura para probar en producción con riesgo controlado.

### 4.3. Estrategias Avanzadas
- **Pruebas A/B (A/B Testing):** Similar al canario, pero con un objetivo de negocio específico. Dos versiones del modelo (A y B) sirven tráfico en paralelo para comparar su efectividad en una métrica (ej. tasa de clics).
- **Sombra (Shadow / Mirroring):** Se despliega v2 en "modo sombra". Recibe una copia del tráfico real de v1, pero sus predicciones no se devuelven al usuario. Sirve para validar el rendimiento de v2 sin impacto en el usuario.
