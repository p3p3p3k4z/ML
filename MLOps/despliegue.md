Esta etapa es el "puente" crítico donde el modelo de Machine Learning deja de ser un experimento en el laboratorio de un científico de datos y se convierte en un servicio funcional que genera valor para el negocio. Para un perfil orientado a **DevOps**, esta es la fase más familiar y, a la vez, la más desafiante debido a la naturaleza cambiante de los datos.

---

## 1. Entornos de Ejecución: El Problema de la Consistencia

El mayor reto al pasar del desarrollo al despliegue es la inconsistencia entre entornos.

- **Entorno de Desarrollo:** Donde el **Data Scientist** usa **datos de entrenamiento** para desarrollar el modelo . Suele tener versiones de librerías actualizadas (ej. Python 3.6, Pandas 1.24) .

- **Entorno de Producción:** Donde el modelo recibe **datos reales** para generar predicciones (ej. "Probabilidad de fuga del 98%") . A menudo, este entorno tiene versiones antiguas o diferentes (ej. Python 2.8, Scikit-learn 0.21), lo que causa fallos catastróficos .

### La Solución: Contenedores

Para garantizar que el modelo funcione igual en cualquier parte, se utilizan **Contenedores** (como Docker) .

- **Beneficios:** Son portátiles, fáciles de mantener y tienen un arranque extremadamente rápido .

- **Escalabilidad:** Permiten iniciar múltiples copias de la misma aplicación fácilmente para manejar más tráfico .

---

## 2. Arquitecturas de Despliegue

La forma en que se estructura el software impacta directamente en cómo se actualiza el modelo.

| **Arquitectura**   | **Descripción**                                                                              | **Impacto en MLOps**                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Monolítica**     | Una aplicación única y uniforme que contiene todos los servicios (Pago, Inventario, UI).<br> | Difícil de actualizar; si el modelo falla, puede caerse toda la aplicación.                                   |
| **Microservicios** | Colección de servicios pequeños e independientes.<br><br>                                    | **Ideal:** Permite desplegar y escalar el modelo de forma independiente sin afectar otros servicios .<br><br> |

---

## 3. Inferencia y APIs (Putting the model to work)

La **Inferencia** es el proceso de enviar nuevos datos de entrada al modelo y recibir una salida o predicción.

- **Flujo de Inferencia:** El sistema envía **Input Data** (ej. ID de cliente, cargos totales) a través de una **API** (Application Programming Interface) hacia la instancia que corre el modelo, recibiendo de vuelta una **Prediction** .
    
- **API:** Actúa como el intermediario que permite que el mundo exterior se comunique con el modelo de ML .
    

---

## 4. Estrategias de Despliegue: Gestión del Riesgo

No todos los modelos se lanzan de la misma forma. Elegir la estrategia correcta depende del riesgo que la empresa esté dispuesta a asumir.

1. **Basic Deployment:** Se reemplaza el modelo viejo por el nuevo directamente . Es sencillo y consume pocos recursos, pero tiene un **riesgo alto** si el modelo falla.
 
2. **Shadow Deployment:** El modelo nuevo recibe los mismos datos que el viejo pero sus predicciones no se envían al usuario final . **Riesgo cero**, pero requiere el **doble de recursos**.

3. **Canary Deployment:** El modelo nuevo se lanza solo para un pequeño grupo de usuarios inicialmente . El **riesgo es pequeño** y el consumo de recursos es medio, aunque es más difícil de implementar.

---

## 5. El Motor de MLOps: CI/CD Pipeline

La automatización es lo que permite que un equipo de ML sea veloz y eficiente.
- **Integración Continua (CI):** Incluye la planificación, codificación, construcción y pruebas del código del modelo .

- **Despliegue Continuo (CD):** Incluye el lanzamiento, despliegue y operación (monitoreo) del modelo en producción .


---

## 6. Escalado y Reutilización

Para que MLOps sea sostenible a largo plazo, se deben automatizar los procesos manuales.

- **Diseño de Proyectos:** El diseño suele ser manual, pero se deben usar **plantillas (templates)** para automatizar y escalar el inicio de nuevos proyectos .

- **Feature Store:** Almacena características ya procesadas. Ahorra tiempo al no tener que construir las mismas variables una y otra vez para diferentes modelos, facilitando el escalado .

- **Experiment Tracking:** Automatiza el seguimiento de versiones de datos, modelos e hiperparámetros para asegurar la **reproducibilidad** .
    

---

### 🚀 Perspectiva de Ingeniería (DevOps)

Como aspirante a **SysAdmin/DevOps**, tu rol en esta fase es configurar los **Pipelines de CI/CD** y gestionar la **Containerización**. Mientras que el científico de datos se preocupa por la _Accuracy_, tú te aseguras de que el modelo tenga **alta disponibilidad** (vía microservicios) y que el despliegue sea seguro (vía estrategias como _Canary_).
