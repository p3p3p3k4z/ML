### Reducción de Dimensionalidad

La "dimensionalidad" se refiere al número de **atributos** (columnas o _features_) en un conjunto de datos. A veces, tener demasiados atributos puede ser un problema ("la maldición de la dimensionalidad").

El objetivo es reducir esta cantidad, lo que implica **eliminar atributos** que no son útiles. Esto se hace por dos razones principales:

- **Irrelevancia:** Algunos atributos pueden ser simplemente **irrelevantes** para la predicción y solo añaden "ruido" que confunde al modelo.
    
- **Correlación:** Algunos atributos tienen una alta correlación, lo que significa que **contienen información muy similar** (son redundantes). Se puede eliminar uno de ellos sin perder mucho poder predictivo.
    

---

### Optimización de Hiperparámetros

Los hiperparámetros son los **ajustes** configurables de un algoritmo de ML que se definen _antes_ de que comience el entrenamiento.

- **Analogía:** Se pueden pensar como los controles de una **consola de música**. No son la música (los datos), sino los botones del ecualizador que **se ajustan dependiendo del "género"** (el tipo de problema).
    
- **Impacto:** Encontrar la combinación correcta de hiperparámetros es crucial. Diferentes configuraciones **proporcionan mejores o peores** resultados y **afectan directamente el rendimiento** final del modelo.
    

---

### Métodos de Ensamble

Esta técnica se basa en la idea de que la **conjunción de distintos modelos** (un "comité" de expertos) puede producir un resultado más preciso y robusto que un solo modelo individual.

En lugar de depender de un solo modelo, se entrenan varios y sus predicciones se combinan.

- **Para la regresión:** Un método común de combinación es **ocupar el promedio** de las predicciones de todos los modelos del ensamble.
    
- **Para la clasificación:** Se suele utilizar una "votación". La clase que predice la mayoría de los modelos es la que se elige como resultado final.