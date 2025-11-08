## Tipos Principales de Machine Learning

Existen varias "familias" de algoritmos en ML, que se diferencian principalmente por _cómo_ aprenden y _qué tipo de datos_ necesitan.

### 🧠 Aprendizaje por Refuerzo (Reinforcement Learning)

Este es el que llamaste "aprendizaje por esfuerzo". El objetivo es que un "agente" (el modelo) aprenda a **tomar decisiones secuenciales** óptimas en un entorno para maximizar una recompensa.

- **Cómo aprende:** El agente aprende a través de prueba y error. Realiza una acción y el entorno le devuelve un "estado" y una "recompensa" (o "castigo"). El modelo aprende qué secuencia de acciones (política) le da la mayor recompensa a largo plazo.
    
- **Ejemplo:** Tu ejemplo es perfecto: **decidir el próximo movimiento de una pieza de ajedrez**.
    
    - _Acción:_ Mover un peón.
        
    - _Recompensa:_ Capturar una pieza (recompensa alta) o perder una (castigo).
        
    - _Objetivo:_ Ganar el juego (recompensa final máxima).
        
- **Relación con la Teoría de Juegos:** Lo mencionaste y es una conexión clave. Ambos campos estudian la toma de decisiones estratégicas, donde el resultado de la acción de un agente depende de las acciones de otros o del estado del entorno.
    

### 🏷️ Aprendizaje Supervisado (Supervised Learning)

Este es el tipo de ML más común. El objetivo es aprender una "función" que mapea entradas a salidas basándose en ejemplos.

- **Cómo aprende:** Se entrena con datos que ya tienen la "respuesta correcta".
    
- **Datos que usa:** Como veremos más adelante, los datos de entrenamiento están **etiquetados**.
    
- **Ejemplos:**
    
    - **Clasificación:** Predecir una categoría (Ej. ¿Es este correo "spam" o "no spam"?).
        
    - **Regresión:** Predecir un valor numérico (Ej. ¿Cuál será el precio de esta casa?).
        

### 📦 Aprendizaje No Supervisado (Unsupervised Learning)

En este caso, el objetivo es encontrar estructura, patrones o relaciones en los datos por nuestra cuenta, sin tener "respuestas correctas" previas.

- **Cómo aprende:** El algoritmo intenta "dar sentido" a los datos por sí mismo.
    
- **Datos que usa:** Los datos de entrenamiento **no están etiquetados**.
    
- **Ejemplos:**
    
    - **Agrupamiento (Clustering):** Tu ejemplo de **agrupar**. (Ej. Agrupar clientes con comportamientos de compra similares).
        
    - **Detección de Anomalías:** Tu ejemplo de **detectar anomalías**. (Ej. Identificar una transacción bancaria fraudulenta que es "diferente" al resto).
        
    - **Reducción de Dimensionalidad:** Simplificar los datos encontrando sus componentes principales.
        

---

## 3. El Pilar: Los Datos de Entrenamiento

Independientemente del tipo de aprendizaje, todo se reduce a los datos.

- **¿Qué son?** Son los **datos existentes de los que el modelo va a aprender**. Son el "libro de texto" del modelo.
    
- **El proceso de entrenamiento:** Mencionaste un punto clave: **"Cuando se construye un modelo a partir de datos de entrenamiento puede tomar su tiempo"**. Esto es crucial. El "entrenamiento" es el proceso computacional de ajustar el modelo a los datos, y puede ser muy intensivo, llevando desde segundos hasta semanas.
    

### La Gran División (Supervisado vs. No Supervisado)

La naturaleza de estos datos define los dos tipos principales de aprendizaje que vimos:

- **Para Aprendizaje Supervisado:** Los datos de entrenamiento **están etiquetados** (o "son conocidos"). Esto significa que cada dato de entrada (o _feature_) tiene una salida o respuesta correcta asociada (la _etiqueta_).
    
    - _Ejemplo:_ `[ (característica_1, característica_2), etiqueta_A ]`, `[ (característica_1, característica_2), etiqueta_B ]`
        
- **Para Aprendizaje No Supervisado:** Los datos de entrenamiento **solo tienen atributos** (features) y no tienen etiquetas. El modelo debe encontrar los patrones por sí mismo.
    
    - _Ejemplo:_ `[ (característica_1, característica_2) ]`, `[ (característica_1, característica_2) ]`
        
