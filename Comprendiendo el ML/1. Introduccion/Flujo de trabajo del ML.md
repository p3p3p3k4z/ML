
Construir un modelo de Machine Learning es un ciclo iterativo.

### Paso 1: Preparación de los Datos

- **Extraer los datos:** Obtener el conjunto de datos inicial.
    
- **Manipulación y selección:** Se deben **elegir los atributos** (features) más relevantes y **manipular el conjunto de datos** (limpieza, formateo, etc.) para prepararlos para el modelo.
    

---

### Paso 2: División del Conjunto de Datos

- El conjunto de datos principal se divide en dos:
    
    - **Conjunto de Entrenamiento (Training Set):** Se usa para que el modelo aprenda.
        
    - **Conjunto de Prueba (Test Set):** Se reserva para la evaluación final.
        

---

### Paso 3: Entrenamiento del Modelo

- Este es el proceso de "aprendizaje".
    
- Consiste en **introducir el conjunto de datos de entrenamiento en un modelo de ML** (un algoritmo específico) para que encuentre patrones.
    

---

### Paso 4: Evaluación e Iteración

- **Evaluar:** Se mide el rendimiento del modelo.
    
- **Iterar:** **Si no se alcanza el rendimiento deseado**, se debe **afinar el modelo** (ajustar sus parámetros) y **repetir el entrenamiento**. Este es un ciclo que continúa hasta que el modelo es satisfactorio.
    

### ¿Cómo Evaluar el Modelo?

La evaluación se realiza sobre datos que el modelo no ha visto antes para obtener una medida honesta de su rendimiento.

- **Usar el Conjunto de Prueba:** Se usan los **datos no vistos** (el _test set_) que se separaron en el Paso 2.
    
- **Métricas Comunes:**
    
    - **Porcentaje de exactitud (Accuracy):** Mide qué fracción de las predicciones fue correcta (común en clasificación).
        
    - **Error promedio de predicción (MAE/RMSE):** Mide qué tan "lejos" están las predicciones del valor real, en promedio (común en regresión).