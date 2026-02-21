# Apuntes de MLOps: Deployment y Ciclo de Vida

## 1. Filosofía Principal: Deployment-Driven Development

El desarrollo debe estar guiado por el objetivo final: la puesta en producción. Esto implica tener en cuenta la operación del modelo desde el inicio.

## 2. Pilares Fundamentales: Transparencia y Reproducibilidad

Sin transparencia y reproducibilidad, un modelo debería ser rechazado ("Return to sender!").

- **Objetivo:** No debe haber ningún dilema sobre cómo se pasa del código y los datos brutos al modelo final.
- **Beneficio:** Recrear el modelo exacto debe ser simple y directo.
- **Buenas prácticas:**
    - Versionado de datasets.
    - Tuberías (pipelines) completamente transparentes.
    - Registro de experimentos en un **metadata store** (puntos extra).

## 3. Principales Preocupaciones (Concerns) en MLOps

El ciclo de vida de un modelo en producción presenta varios desafíos clave:

### 3.1. Validación de Datos de Entrada
- **Riesgo:** Clientes se quejan, aunque ellos mismos enviaron entradas erróneas al modelo.
- **Solución:** Implementar validación de datos en el punto de entrada.

### 3.2. Deterioro del Rendimiento (Performance Deterioration)
- **Riesgo:** No hay manera de identificar que los datos han cambiado (deriva de datos) y que nuestro modelo ya no es válido.
- **Requisito mínimo:** Registrar (loguear) las entradas y salidas del modelo para poder detectar desviaciones.

### 3.3. Depuración (Debugging)
- La capacidad de depurar problemas en producción es esencial y se ve facilitada por un buen registro de datos y transparencia.

### 3.4. Confianza en el Código
- **Pregunta clave:** ¿Me siento cómodo haciendo cambios en este código?
- **Requisito:** Implementar una suite de pruebas para generar confianza y robustez:
    - Pruebas unitarias
    - Pruebas de integración
    - Pruebas de carga
    - Pruebas de estrés
    - Pruebas de despliegue

## 4. Componentes y Prácticas Esenciales

### 4.1. Perfilado de Datos (Data Profiling)
- **Definición:** Análisis automatizado de datos para la creación de resúmenes de alto nivel (perfiles o expectativas).
- **Uso:** Validar y monitorear datos en producción.
- **Objetivos:**
    1.  Retroalimentación al usuario.
    2.  Decisiones de reentrenamiento.
- **Herramienta destacada:** **Great Expectations**.

### 4.2. Checklist de la Tubería de ML (ML Pipeline Checklist)
Una tubería de entrenamiento robusta debe incluir:

- [ ] ¿Está el código versionado?
- [ ] ¿Están los datos versionados?
- [ ] Entrenar el modelo
- [ ] Guardar el modelo
- [ ] **Crear un perfil de datos** (data profile)
- [ ] **Registrar la versión exacta de los datos de entrenamiento**

### 4.3. Control de Versiones de Datos
- Es tan importante como el versionado de código. Herramientas como DVC (Data Version Control) ayudan a gestionarlo.

### 4.4. Almacén de Características (Feature Store)
- **Definición:** Esencialmente una base de datos centralizada para características (features).
- **Beneficios:**
    1.  **Reutilización:** Las mismas features pueden ser usadas por diferentes equipos y modelos.
    2.  **Consistencia:** Reduce la desviación entre entrenamiento y servicio (train/serve skew). La feature que se usa para entrenar es la misma que se calcula en producción.

## 5. Tuberías de Construcción (Build Pipelines) en CI/CD

En ML existen dos tipos principales de pipelines de construcción:

1.  **Pipeline de la Aplicación:** Construye la app que sirve el modelo (Pipeline de software estándar).
2.  **Pipeline del Modelo (Model BUILD Pipeline):** Construye (entrena) el modelo. Este es el núcleo del framework MLOps.
    - **Ecuación:** `MODEL pipeline = model BUILD pipeline`
    - **Beneficios:**
        - ✓ Despliegue (Deployment)
        - ✓ Reproducibilidad
        - ✓ Monitoreo
        - ✓ Integración con CI/CD

## 6. Reproducibilidad y Confianza

- **Ecuación clave:** `Reproducibilidad = Control = Confianza`
- **Checklist de Reproducibilidad:**
    - [ ] Puntero a la versión exacta del código del pipeline de construcción del modelo.
    - [ ] Puntero a las versiones exactas de los datasets usados (incluyendo los splits de entrenamiento/validación/test).
    - [ ] Registro del rendimiento obtenido en el conjunto de prueba (test set).

## 7. Empaquetado de Modelos

### Opciones de Almacenamiento

| Formato | Ventajas (PROs) | Desventajas (CONs) |
| :--- | :--- | :--- |
| **Formato Universal (Ej. ONNX)** | Universal. Entrenar en un lenguaje, servir en otro completamente diferente. | Difícil de personalizar. |
| **.pickle (Python)** | Ecosistema Python. No es específico de ML, puede guardar cualquier objeto. | Sin compatibilidad multiplataforma. Los entornos de entrenamiento y servicio deben ser idénticos. |

**Recomendación si usas .pickle:**
> "IF model_format == .pickle THEN: store list of model's dependencies within model package and verify server compatibility when loading"

## 8. Monitoreo y Despliegue Final

- **Checklist de Monitoreo:**
    - [ ] Perfil de datos de entrada (Input data profile)
    - [ ] Perfil de datos de salida (Output data profile)
- **Fase Final:** **"Lock 'n' load!"** - Preparados para poner el modelo en producción con todas las garantías.