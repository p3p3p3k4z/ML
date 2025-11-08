El aprendizaje supervisado se basa en **datos de entrenamiento etiquetados**. El modelo aprende la relación entre las _features_ (entradas) y las _etiquetas_ (salidas) para poder predecir la etiqueta de datos nuevos. Se puede pensar en el modelo como una **"máquina de etiquetado"** que aprende con ejemplos.

Este tipo de aprendizaje tiene dos tareas principales: Clasificación y Regresión.

---

### 🎯 Clasificación

El objetivo es **asignar una categoría** a una observación.

- **¿Qué predice?** Una **variable discreta**, es decir, un valor que pertenece a un grupo limitado (que tiene "pocos valores"). La salida es una etiqueta.
    
- **Ejemplo:** A partir de sus medidas, ¿cuál es esta flor?: ¿lirio, tulipán o clavel?
    
- **Proceso:**
    
    - Se **alimenta el modelo con observaciones** donde cada una ya ha sido etiquetada (ej. "esto es un lirio").
        
    - El **objetivo** es **crear un "gráfico"** o frontera de decisión que permita **dividir los datos** y, en el futuro, **clasificar** nuevas observaciones.
        
- **Algoritmos de Ejemplo:** **Máquina de Vectores de Soporte (SVM)**, que funciona como un **clasificador lineal** o puede usar núcleos (como el **polinómico**) para fronteras más complejas.
    

---

### 📈 Regresión

El objetivo es **asignar una variable continua**.

- **¿Qué predice?** Un número que **puede tener (casi) cualquier valor** dentro de un rango.
    
- **Ejemplos:** "¿Qué masa tiene este exoplaneta?" o "¿Cuál será la temperatura mañana?".
    
- **Proceso (Flujo de ejemplo):**
    
    1. **Datos de Entrenamiento:** Se usan datos históricos (ej. del clima).
        
    2. **Algoritmo:** Se selecciona un algoritmo (ej. **Regresión Lineal**).
        
    3. **Modelo:** El algoritmo "aprende" la tendencia y genera un modelo.
        
    4. **Predicción:** Se usa el modelo para **encontrar la temperatura** de un día futuro.
        
- **Punto Clave:** **Al añadir más elementos** (o _features_ relevantes, como la humedad o el viento en el ejemplo de la temperatura), la predicción puede volverse **más predecible** y precisa.