## Métodos de Ensamble (Ensemble Methods) en Spark ML 🌳🌲🌳

Los métodos de ensamble son una técnica avanzada y poderosa en Machine Learning que se basa en una idea simple pero efectiva: **la unión hace la fuerza**.

-----

### Concepto Clave: El "Comité" de Expertos

  * **Definición:** Un ensamble consiste en crear una **colección de modelos** (a menudo llamados "estimadores base" o "aprendices débiles") y **combinar sus resultados** para obtener una predicción final única.
  * **Analogía:** Piensa en un **comité**. La decisión tomada por un grupo de expertos diversos suele ser mejor y más robusta que la decisión de un solo individuo, por muy inteligente que sea.
  * **Sabiduría de la multitud (Wisdom of the Crowd):** Si los modelos individuales son ligeramente mejores que el azar y son lo suficientemente diversos e independientes, su combinación puede producir predicciones mucho más precisas.
  * **Diversidad:** Para que el comité funcione, sus miembros deben pensar diferente. En ML, **entre más diversos sean los modelos, mejor** será el ensamble. Si todos cometen los mismos errores, el ensamble no mejora nada.

Existen dos familias principales de métodos de ensamble: **Bagging** (ej. Random Forest) y **Boosting** (ej. Gradient-Boosted Trees).

-----

### 1\. Random Forest (Bosque Aleatorio) - Bagging 🎒

Random Forest es el ejemplo clásico de la técnica **Bagging** (Bootstrap Aggregating). Su objetivo es reducir la varianza (hacer el modelo más estable y menos propenso al sobreajuste).

  * **¿Cómo funciona?**

    1.  Crea muchos árboles de decisión independientes.
    2.  Cada árbol se entrena con un **subconjunto aleatorio diferente de los datos** (muestreo con reemplazo o *bootstrapping*).
    3.  Además, en cada nodo de cada árbol, se considera solo un **subconjunto aleatorio de características** para hacer la división. Esto garantiza aún más **diversidad** e independencia entre los árboles.
    4.  **Paralelismo:** Como los árboles son independientes, **se pueden entrenar en paralelo**, lo que lo hace muy rápido y escalable.
    5.  **Predicción Final:**
          * *Clasificación:* Votación por mayoría (la clase que más árboles predijeron).
          * *Regresión:* Promedio de las predicciones de todos los árboles.

  * **En Spark ML:**

    ```python
    from pyspark.ml.classification import RandomForestClassifier

    # Crear el bosque
    # numTrees: cuántos árboles (miembros del comité) queremos.
    forest = RandomForestClassifier(numTrees=5)

    # Entrenar (los 5 árboles se entrenan en paralelo si es posible)
    forest_model = forest.fit(cars_train)
    ```

  * **Inspección:** Podemos incluso ver los árboles individuales dentro del bosque.

    ```python
    # Ver los árboles individuales
    print(forest_model.trees)
    ```

  * **Importancia de Características:** Random Forest nos dice qué características fueron más útiles para tomar decisiones.

    ```python
    # Ver la importancia de cada característica
    print(forest_model.featureImportances)
    ```

-----

### 2\. Gradient-Boosted Trees (GBT) - Boosting 🚀

Gradient-Boosted Trees utiliza la técnica de **Boosting**. Aquí, los modelos no son independientes; trabajan en equipo secuencialmente para reducir el sesgo (mejorar la precisión).

  * **¿Cómo funciona?**

    1.  Entrena una **secuencia de modelos** (árboles), uno tras otro.
    2.  Cada modelo nuevo **intenta corregir los errores** cometidos por la combinación de los modelos anteriores. Se enfoca en los casos "difíciles" que los otros no pudieron resolver bien.
    3.  **Secuencial:** NO se pueden entrenar en paralelo, porque el árbol 2 necesita saber qué tan mal lo hizo el árbol 1. Esto puede hacerlo más lento de entrenar que Random Forest.
    4.  **Mejora Iterativa:** El modelo mejora con cada iteración, pero también tiene mayor riesgo de sobreajuste si se usan demasiadas.

  * **En Spark ML:**

    ```python
    from pyspark.ml.classification import GBTClassifier

    # Crear el modelo GBT
    gbt = GBTClassifier(maxIter=10) # 10 árboles secuenciales

    # Entrenar (debe ser secuencial)
    gbt_model = gbt.fit(train_data)
    ```

-----

### Comparación de Rendimiento

Ambos métodos suelen superar a un simple árbol de decisión.

  * **Árbol de Decisión:** Simple, interpretable, pero propenso a sobreajuste.
  * **Random Forest:** Robusto, paralelizable, bueno "casi siempre" sin mucho ajuste.
  * **GBT:** A menudo puede lograr una precisión ligeramente mayor que Random Forest si se ajusta bien, pero es más lento de entrenar y más sensible a los hiperparámetros.

*(En la imagen de ejemplo, tanto RF como GBT superan al árbol simple, con un AUC de 0.65 vs 0.58)*.