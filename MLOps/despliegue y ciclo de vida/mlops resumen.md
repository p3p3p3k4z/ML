# MLOps: Despliegue y Ciclo de Vida del Modelo

## 1. Definición y Objetivos de MLOps

MLOps (Machine Learning Operations) no es solo una herramienta, sino un conjunto de **principios, prácticas y herramientas**. Su objetivo principal es transformar los flujos de trabajo de ML en servicios que sean:

- **Automatizados:** Reducir la intervención manual para ganar velocidad y consistencia.
    
- **Reproducibles:** Capacidad de recrear resultados exactos en cualquier momento.
    
- **Integrados:** Conectar todas las piezas del rompecabezas de datos y código.
    

## 2. La Necesidad de MLOps: Deuda Técnica

El punto de partida habitual en muchas empresas son flujos de trabajo manuales y monitoreo _ad hoc_. Esto genera **Deuda Técnica**, definida como el costo implícito de retrabajo causado por elegir una solución fácil y limitada ahora, en lugar de un enfoque mejor que tomaría más tiempo.

+1

- **El Riesgo:** A medida que se despliegan más modelos sin MLOps, el proceso se vuelve más lento, propenso a errores y frustrante, perjudicando la capacidad de entregar valor real al negocio.
    

## 3. Jerarquía de Ciclos de Vida en ML

Es fundamental distinguir entre los tres niveles de ciclos que coexisten en una organización:

1. **Ciclo de Vida del Proyecto:** Desde la definición del problema hasta la entrega de valor.
    
2. **Ciclo de Vida de la Aplicación:** El software general donde reside el modelo.
    
3. **Ciclo de Vida del Modelo:** El enfoque central de este curso, que trata el objeto entrenado como una entidad viva.
    

---

## 4. Etapas del Ciclo de Vida del Modelo

A diferencia de un objeto teórico, en MLOps un **modelo** es una entidad concreta y entrenada lista para entrar en uso.

### A. Entrenamiento y Empaquetado

- El modelo pasa de ser código a un objeto binario.
    
- **Paquete de Despliegue:** Consiste en el objeto del modelo más los recursos de infraestructura necesarios (librerías, scripts de entorno).
    

### B. Despliegue e Inferencia

- **Despliegue:** Es el acto de poner el modelo en uso real.
    
- **Inferencia:** El proceso donde el modelo recibe datos nuevos y genera predicciones.
    

### C. Monitoreo Post-Despliegue

Se enfoca en responder dos preguntas críticas:

1. ¿Está funcionando el servidor del modelo? (Salud de la infraestructura).
    
2. ¿Son las entradas y salidas las esperadas? (Salud estadística/Drift).
    

### D. Desmantelamiento (Decommissioning) y Archivado

Un modelo sale de producción cuando aparece uno mejor, se crean características más informativas o el proceso modelado cambia drásticamente.

- **Archivado:** Es vital en industrias reguladas para responder por qué se tomó una decisión en el pasado (ej. aprobación de un crédito en 2020). Requiere una alta **reproducibilidad**.
    

---

## 5. Componentes del Framework MLOps: Almacenes y Registros

Para gestionar la complejidad, el framework se divide en conceptos genéricos de software y específicos de ML.

+1

### Componentes Específicos de ML (Registros y Almacenes)

Estos son los pilares que mencionaste y que permiten la escalabilidad:

+1

- **Model Registry (Registro de Modelos):** Un catálogo centralizado para gestionar las versiones de los modelos. Permite rastrear quién entrenó el modelo, con qué datos y su estado actual (staging, producción, archivado).
    
- **Feature Store (Almacén de Características):** Un repositorio donde se guardan las variables ya procesadas (features). Su objetivo es evitar que diferentes científicos de datos calculen la misma variable dos veces y garantizar que se usen las mismas definiciones tanto en entrenamiento como en producción.
    
- **Metadata Store (Almacén de Metadatos):** Registra toda la información sobre las ejecuciones de los pipelines: hiperparámetros usados, métricas obtenidas (accuracy, RMSE), fecha de ejecución y enlaces a los artefactos generados. Es el "diario de bitácora" del sistema.
    

### Conceptos Genéricos Aplicados

- **Workflows (Flujos de trabajo):** La secuencia lógica de pasos (ej. limpieza -> entrenamiento -> evaluación).
    
    +2
    
- **Pipelines:** La implementación automatizada de esos flujos.
    
- **Artifacts (Artefactos):** Cualquier archivo generado en el proceso, como el modelo entrenado, gráficos de evaluación o archivos de datos procesados.
    
    +1
    

---

## 6. Madurez de MLOps

La madurez de una organización no se mide por la complejidad de sus modelos, sino por el **nivel de automatización de sus flujos de trabajo**. Una implementación completa de MLOps garantiza procesos que son rápidos, reproducibles y explicables.