Llegamos a la fase de **Mantenimiento y Monitoreo**, el componente que cierra el ciclo de vida de MLOps y garantiza que el modelo siga siendo útil a lo largo del tiempo. Como aspirante a **SysAdmin/DevOps**, esta sección es vital, ya que aquí es donde se integran las métricas de infraestructura con las métricas de salud del modelo.

---

## I. Tipos de Monitoreo en MLOps

El monitoreo no se limita a saber si el servidor está "vivo"; en ML, debemos vigilar tanto la infraestructura como la integridad de las predicciones.

### 1. Monitoreo Estadístico (Data-Centric)

Se enfoca en los datos de entrada y salida, incluyendo las predicciones del modelo.

- **Ejemplo:** Vigilar que las probabilidades de _churn_ (fuga de clientes) se mantengan en rangos esperados (ej. Cliente X tiene 72% de probabilidad).
    

### 2. Monitoreo Computacional (Ops-Centric)

Se enfoca en métricas técnicas tradicionales, fundamentales para el perfil de Operaciones.

- **Métricas clave:** Uso de CPU del servidor, número de solicitudes entrantes, cantidad de predicciones por segundo y tiempo de inactividad (_downtime_).
    

---

## II. Degradación del Modelo: ¿Por qué fallan?

A diferencia del software tradicional, un modelo de ML puede fallar gradualmente aunque el código esté intacto. Esto se debe al fenómeno del **Drift** (Deriva).

- **Data Drift (Deriva de Datos):** Ocurre cuando hay cambios significativos en los **datos de entrada** que recibe el modelo.
    
- **Concept Drift (Deriva de Concepto):** Ocurre cuando cambia la **relación** entre los datos de entrada y el objetivo (output). Por ejemplo, un modelo que predice hábitos de compra antes y después de una pandemia.
    
### El Ciclo de Retroalimentación (Feedback Loop)

Es el proceso mediante el cual se utiliza la **"verdad real"** (_ground truth_) para mejorar y ajustar el modelo de forma continua.

---

## III. Estrategia de Reentrenamiento

El reentrenamiento consiste en utilizar datos nuevos para desarrollar una versión fresca y actualizada del modelo.

Factores para decidir la frecuencia de reentrenamiento:

1. **Entorno de negocio:** ¿Qué tan volátiles son los datos?
    
2. **Costo:** ¿Cuánto cuesta procesar y entrenar la nueva versión?
    
3. **Requisitos de negocio:** ¿Cuál es el nivel mínimo de rendimiento aceptable?
    

---

## IV. Niveles de Madurez en MLOps

La madurez define qué tan automatizados y colaborativos son los procesos de una empresa.

- **Nivel 1: Procesos Manuales.** Desarrollo y despliegue manual, equipos aislados (Silos), sin rastreo ni monitoreo.
    
- **Nivel 2: Desarrollo Automatizado.** Pipeline de CI (Integración Continua) automatizado, pero despliegue manual. Existe rastreo de experimentos y características.
    
- **Nivel 3: Automatización Total (CI/CD).** Desarrollo y despliegue (CD) automatizados. Colaboración estrecha entre equipos y **reentrenamiento automático** disparado por el monitoreo.
    

---

## V. El Toolkit Profesional de MLOps

Para implementar lo anterior, el ecosistema cuenta con herramientas especializadas:

|Categoría|Herramientas Citadas|Propósito|
|---|---|---|
|**Feature Store**|Feast, Hopsworks|Almacenar y reutilizar características.|
|**Rastreo (Tracking)**|MLFlow, ClearML, W&B|Visualizar y reproducir experimentos.|
|**Containerización**|Docker, Kubernetes|Empaquetar y orquestar aplicaciones.|
|**CI/CD Pipeline**|Jenkins, GitLab|Automatizar la integración y despliegue.|
|**Monitoreo**|Fiddler, Great Expectations|Vigilar modelos y calidad de datos.|
|**Plataformas Cloud**|AWS SageMaker, Azure ML, Google Vertex AI|Ciclo de vida completo en la nube.|
supervision: great expectations fiddler

---

### 🛠️ Perspectiva de Ingeniería (SysAdmin/DevOps)

Como aspirante a **SysAdmin/DevOps**, tu rol en esta fase es configurar alertas automáticas. Si el **Monitoreo Computacional** detecta un pico de CPU, es un problema de infraestructura. Pero si el **Monitoreo Estadístico** detecta **Data Drift**, el sistema debe ser capaz de disparar automáticamente un pipeline de reentrenamiento (Nivel 3 de madurez). Herramientas como **Kubernetes** para la orquestación y **Jenkins/GitLab** para la automatización son tus herramientas principales en este campo.