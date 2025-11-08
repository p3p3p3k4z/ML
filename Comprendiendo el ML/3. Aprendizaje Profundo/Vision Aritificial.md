La Visión Artificial es un campo de la Inteligencia Artificial que busca **ayudar a las computadoras a "ver" y comprender el contenido de las imágenes digitales** (como fotos y videos) de una manera similar a como lo hacen los humanos.

---

### ¿Cómo "ve" una Computadora? Los Píxeles

Una imagen digital está formada por una cuadrícula de miles o millones de **píxeles**. Cada píxel contiene información numérica sobre la **intensidad** (en blanco y negro) y el **color**.

- **Imágenes a Color (RGB):** Comúnmente, el color se almacena usando el modelo **RGB** (Rojo, Verde, Azul). Esto significa que la imagen se representa en **3 "tramas"** (o matrices/canales). Hay una matriz que indica la intensidad del rojo en cada píxel, una para el verde y otra para el azul.
    
- **Datos para el ML:** Estos **números** (los valores de los píxeles) son los datos brutos que se utilizan como entrada para un modelo de Machine Learning.
    

---

### ¿Cómo "entiende" una Computadora? Deep Learning

La técnica más exitosa para la Visión Artificial es el Aprendizaje Profundo (Deep Learning), específicamente usando **Redes Neuronales Convolucionales (CNNs)**.

Estas redes imitan la jerarquía visual humana. Como mencionaste en tu apunte, el proceso es el siguiente:

1. **Capas Iniciales:** Las primeras capas de neuronas (las del "principio") aprenden a detectar patrones muy simples, como **bordes**, líneas rectas, esquinas y curvas.
    
2. **Capas Intermedias:** Combinan esos bordes para reconocer formas más complejas, como círculos, cuadrados o texturas.
    
3. **Capas Finales:** Las neuronas del "final" combinan esas formas complejas para reconocer objetos completos o partes de ellos, como **caras**, ojos, ruedas de un auto o un gato.
    

---

### Tareas y Aplicaciones Comunes

La Visión Artificial permite realizar tareas específicas que tienen aplicaciones en el mundo real.

#### Tareas Principales

- **Clasificación:** ¿Qué es el objeto principal en esta imagen? (Ej. "Es un gato").
    
- **Detección de Objetos:** ¿Qué objetos hay y dónde están? (Dibuja una caja alrededor de cada objeto, como en tu ejemplo de "detección de objetos").
    
- **Segmentación:** Delinea el contorno exacto de cada píxel que pertenece a un objeto.
    

#### Aplicaciones Reales

- **Vehículos Autónomos:** Para detectar peatones, otros autos, señales de tráfico y carriles.
    
- **Medicina:** **Detección de tumores** o anomalías en imágenes médicas (Rayos X, resonancias magnéticas).
    
- **Seguridad:** **Reconocimiento facial** para desbloquear dispositivos o para vigilancia.
    
- **Realidad Aumentada:** Superponer información digital sobre el mundo real.