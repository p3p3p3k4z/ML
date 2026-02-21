# Apuntes de MLOps: Monitoreo, Mantenimiento y Gobernanza

## 1. Monitoreo de Servicios ML: Manteniendo la Calidad

Los clientes que pagan tienen expectativas de calidad. La garantía de calidad comienza con el control de calidad, y el control de calidad en producción se llama **monitoreo**.

### 1.1. Indicadores a Monitorear

Es crucial separar la salud del sistema del rendimiento del modelo.

- **Indicadores Fundamentales de Salud (Infraestructura):**
    - ¿El servicio está funcionando (up and running)?
    - Número de solicitudes en el tiempo (throughput).
    - Distribución de la latencia (percentiles p95, p99).
- **Métrica de Calidad Última (Rendimiento Predictivo):**
    - ¿Cómo se deterioran los modelos con el tiempo?
    - Este es el foco principal del monitoreo en MLOps.

---

## 2. La Gran Amenaza: La Deriva de Conceptos (Concept Drift)

El mayor enemigo de un modelo en producción es el cambio en los datos del mundo real.

### 2.1. El Problema: El Mundo Cambia
1.  **Entrenamiento:** El modelo aprende la relación entre las características de entrada (*features*) y la variable objetivo (*label*) basándose en datos históricos.
2.  **Modelo Entrenado:** Se despliega un modelo que ha "aprendido" una función específica del pasado.
3.  **Tiempo Después (After a While)...** : La relación subyacente entre las entradas y las salidas cambia en el mundo real.
    - **Concept Drift (Deriva de Concepto):** Es el cambio significativo en la relación real entre las características de entrada y la variable de salida. El modelo se vuelve obsoleto porque el "concepto" que aprendió ya no es válido.

### 2.2. Cómo Detectar la Deriva de Concepto

- **Enfoque Directo (Ideal):**
    > `IF predicción != valor_real (ground truth) MÁS A MENUDO DE LO ESPERADO THEN ALERTA("¡DERIVA DE CONCEPTO!")`
- **El Problema (The Catch):**
    - En muchos casos, el **valor real (ground truth)** no está disponible de inmediato (o nunca lo está).
    - **Ejemplo:** En detección de fraude, ¿cómo saber si una transacción fue realmente fraudulenta? Pueden pasar meses hasta que el cliente lo reporte.
    - **Ejemplo:** En un sistema de recomendaciones, ¿cuál es el "label" correcto para una recomendación que no fue clickeada? Tal vez no era relevante, o tal vez el usuario solo tenía prisa.

### 2.3. Enfoque Indirecto: Monitorear las Entradas

Dado que la salida ideal (ground truth) no siempre está disponible, se monitorea lo que sí se tiene: **las características de entrada (input features)** .

- **Objetivo:** Detectar **Data Drift (Deriva de Datos)** .
- **Mecanismo:** Se compara la distribución estadística de los datos de entrenamiento con la distribución de los datos que está recibiendo el modelo en producción.
- **Suposición:** Si los datos de entrada han cambiado significativamente (deriva de datos), es muy probable que el rendimiento del modelo también se haya visto afectado (deriva de concepto).

### 2.4. Limitaciones del Monitoreo de Entradas

El enfoque indirecto no es perfecto. Las principales limitaciones son:

- **Demasiado Sensible:** Puede generar alertas por cambios estadísticos irrelevantes para el rendimiento del modelo.
- **Poco Informativo:** Un cambio en los datos de entrada no te dice con certeza cuánto ha empeorado el modelo. Solo te dice que *podría* haber empeorado.

---

## 3. Infraestructura de Monitoreo y Alertas

Un sistema de monitoreo eficaz se compone de varios elementos que trabajan juntos.

### 3.1. Componentes Clave
- **Servicio ML (ML Service):** El sistema en producción que recibe solicitudes del mundo exterior.
- **Registros (Logs):** Toda la información sobre las solicitudes, predicciones, y el comportamiento del sistema se guarda de forma estructurada. Estos logs son la materia prima para el monitoreo.
- **Infraestructura de Monitoreo:** Un sistema separado que procesa los logs para generar métricas y visualizaciones.
- **Pipeline de Datos/ML:** Los datos monitorizados pueden (y deben) realimentar el pipeline de reentrenamiento para mejorar el modelo.

### 3.2. El Desafío de las Alertas (Alerting)
El objetivo del monitoreo es generar alertas cuando algo va mal. Sin embargo, la validación estadística conlleva riesgos:

- **Demasiadas Alertas ("Alert Fatigue"):**
    - Si el sistema es demasiado sensible, generará muchas alertas.
    - El equipo se acostumbra a ignorarlas (fatiga de alertas).
    - **Riesgo:** Las alertas importantes pasan desapercibidas entre el ruido.
- **Solución:** Calibrar cuidadosamente los umbrales y utilizar técnicas más sofisticadas que una simple comprobación de límites.

> **Dato Real:** Un estudio sobre una gran pipeline de ML durante una década reveló la multitud de formas en que los sistemas ML pueden fallar, subrayando la necesidad de un monitoreo robusto. (Referencia: "How ML Breaks: A Decade of Outages for One Large ML Pipeline", USENIX).

---

## 4. Mantenimiento del Modelo: Reaccionar y Mejorar

Cuando se detecta una anomalía o un fallo, comienza el proceso de mantenimiento.

### 4.1. ¿Rendimiento Deteriorado? Dos Enfoques

Tradicionalmente, la respuesta era probar nuevos modelos o nuevas características derivadas. Esto es un enfoque **"Model-centric"** , típico de competiciones (Kaggle) donde el dataset es fijo.

Sin embargo, el mantra moderno de MLOps es: **"Calidad por encima de cantidad" (Quality above quantity)** .

### 4.2. Enfoque Data-Centric (Centrado en los Datos)
- **Obtener más características con información relevante:** En lugar de crear 100 features derivadas sin sentido, buscar 1 o 2 nuevas fuentes de datos que realmente aporten señal.
- **Obtener mejores etiquetas (Labels):**
    - **Label:** Es el valor de la variable objetivo en el conjunto de entrenamiento.
    - **Calidad de la etiqueta:** Es la cercanía de esa etiqueta al valor real (ground truth).
- **Uso de Herramientas de Etiquetado:** El etiquetado manual es complejo, largo y propenso a errores. Las buenas herramientas de etiquetado ayudan a:
    - Ser más eficientes.
    - Ser más precisos (UI adecuada, sugerencias).
    - Priorizar: "Etiqueta estos ejemplos primero para máximo impacto".
    - Corregir: "Parece que cometiste un error aquí".

### 4.3. Sistema Human-in-the-Loop (Persona en el Circuito)
Un enfoque muy efectivo para el mantenimiento es integrar la supervisión humana.
1.  **Modelo en producción** recibe una solicitud con baja confianza o que no cumple con el perfil de datos esperado.
2.  El sistema deriva el caso a un **humano (experto)** .
3.  El humano proporciona la **etiqueta correcta (ground truth)** .
4.  Esta nueva pareja (input, label) se guarda como un **nuevo ejemplo para la mejora del modelo**.
5.  En el próximo ciclo de entrenamiento, este nuevo ejemplo se incorpora al dataset, mejorando el modelo.

### 4.4. Automatización del Reentrenamiento
El proceso de mejora puede (y debe) ser automatizado:
1.  **Ejecutar el pipeline de construcción del modelo (ML Build Pipeline)** con los nuevos datos (mejores etiquetas, nuevas fuentes) para obtener un nuevo modelo.
2.  **Comparar:** ¿Es el nuevo modelo mejor que el antiguo?
    - **SÍ:** Pasar a pruebas y desplegar.
    - **NO:** Seguir buscando (nuevos modelos, features, fuentes de datos).

**Herramienta Clave:** Un **Metadata Store (ej. MLflow Tracking)** es inmensamente útil aquí para documentar el viaje de selección del modelo y evitar repetir experimentos fallidos.

---

## 5. Gobernanza de Modelos: El Marco de Control

A medida que la IA se aplica en sectores críticos (salud, finanzas, legislación, automoción), la gobernanza se vuelve esencial para minimizar riesgos.

### 5.1. Definición
> "La gobernanza de modelos de IA/ML es el proceso general por el cual una organización controla el acceso, implementa políticas y rastrea la actividad de los modelos y sus resultados. La gobernanza de modelos efectiva es la base para minimizar el riesgo, tanto para los resultados de una organización como para su marca." - **DataRobot.com**

### 5.2. Preguntas Clave y Documentación
Un modelo no es solo un archivo `.pkl`. Es un conjunto de decisiones y procesos que deben ser auditables.

- **Ética y Sesgo:**
    - ¿Es ético usar ML en este contexto?
    - ¿Se utilizan datos privados o sensibles?
    - ¿El modelo tiene un sesgo no ético (racial, de género, etc.)?
- **Documentación del Proceso:**
    - Documentos de selección del modelo.
    - Preparación de datos de entrenamiento.
    - Aseguramiento de la calidad (QA).
    - Versionado y reproducibilidad (ver capítulo 2).
- **Seguridad y Operaciones:**
    - ¿La API es segura?
    - ¿El monitoreo está en su lugar?
    - ¿El sistema de alertas funciona?
    - ¿Hay un plan para el manejo de fallos?

### 5.3. Categorías de Riesgo
- **Impacto Financiero:** Pérdidas económicas por malas predicciones (ej. trading algorítmico).
- **Impacto Reputacional:** Daño a la marca por un modelo que actúa de manera injusta o incorrecta.

### 5.4. Resumen
- La gobernanza significa pasos extras, pero la alternativa es la anarquía.
- El objetivo no es "lanzar muchos modelos rápido", sino generar valor de negocio.
- Un ML imprudente causa más daño que beneficio.
- Cuantos más modelos tenga una organización, más obvio se vuelve el beneficio de la gobernanza.

---

## 6. Conclusión y Filosofía MLOps

El curso concluye con los pilares fundamentales y una visión de crecimiento.

### 6.1. Los 5 Pilares (#hashtags)
1.  **#automation** (Automatización)
2.  **#collaboration** (Colaboración entre equipos)
3.  **#efficiency** (Eficiencia en los procesos)
4.  **#transparency** (Transparencia y trazabilidad)
5.  **#user-satisfaction** (Satisfacción del usuario final)

### 6.2. La Hoja de Ruta: "Empieza pequeño y crece"
No intentes implementar todo el arsenal de MLOps el primer día.

- **Tu framework MLOps hoy:** Puede ser algo simple, con scripts manuales y un par de checks. (Diagrama simple y pequeño).
- **Tu framework MLOps en cinco años:** A medida que crecen los modelos, los equipos y el impacto, el framework se vuelve más complejo, con pipelines automatizados, monitoreo sofisticado, feature stores, etc. (Diagrama grande e interconectado).

**La clave es la evolución, no la revolución.**