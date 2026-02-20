En este primer paso para limpiar el conjunto de datos `music_df`, realizaremos un diagnóstico inicial. Antes de construir cualquier modelo o aplicar técnicas de imputación, es fundamental cuantificar cuántos "huecos" (valores `NaN`) tiene cada característica. Esto nos permitirá decidir, basándonos en la regla del 5%, qué columnas podemos limpiar por eliminación y cuáles requerirán una estrategia más avanzada.

```python
# Imprimir los valores faltantes por cada columna
# .isna() identifica los nulos, .sum() los cuenta y .sort_values() los ordena ascendentemente
print(music_df.isna().sum().sort_values())
```

---

### Análisis del Diagnóstico de Datos

Como ingeniero, este es tu primer punto de control en cualquier tubería de datos (_data pipeline_). Aquí te explico por qué este comando es tan potente:

- **Identificación de Patrones:** Al ordenar de forma ascendente, ves inmediatamente qué columnas están "limpias" y cuáles podrían ser problemáticas. Si una columna tiene muchísimos valores faltantes, eliminar las filas podría sesgar el modelo o dejarnos sin datos suficientes para entrenar.
    
- **La Regla del 5%:** Si el conjunto de datos tiene 1,000 filas (como en este caso), cualquier columna con menos de 50 valores faltantes se considera candidata para la eliminación directa (`.dropna()`). Esto simplifica el preprocesamiento sin sacrificar la integridad estadística del dataset.
    
- **Preparación para la Imputación:** Las columnas que superen ese 5% de valores nulos no se eliminarán; en el siguiente paso, definiremos cómo rellenar esos huecos (usando la media o la moda) para que el modelo no pierda esa valiosa información.

---
Una vez identificado qué columnas tienen una cantidad mínima de datos faltantes, aplicamos la técnica de **eliminación selectiva**. En este caso, como el dataset original tiene 1,000 filas, el 5% equivale a 50 registros. Eliminar estas filas es una forma eficiente de limpiar el ruido inicial sin comprometer la estructura de nuestro modelo KNN.

```python
# 1. Visualizar el conteo de nulos (Paso anterior para referencia)
print(music_df.isna().sum().sort_values())

# 2. Eliminar filas con nulos en las columnas que cumplen la regla del < 5%
# Especificamos las columnas en el argumento 'subset'
music_df = music_df.dropna(subset=["genre", "popularity", "loudness", "liveness", "tempo"])
```

---

### Análisis de la Eliminación Selectiva

Como aspirante a **SysAdmin y DevOps**, sabes que la eficiencia en el procesamiento es clave. Aquí te explico por qué usamos `subset` en lugar de borrar todo:

- **Precisión con `subset`**: Si usáramos simplemente `music_df.dropna()`, Pandas eliminaría cualquier fila que tuviera **al menos un** valor nulo en **cualquier** columna. Esto podría hacernos perder muchísima información de columnas que sí planeamos imputar después (como las que tienen más de 50 nulos).
    
- **La Regla del 5% en Producción**: Eliminar datos es una decisión drástica. En ingeniería de datos, se considera que perder menos del 5% de las muestras es un "costo aceptable" a cambio de no introducir ruido artificial (imputaciones) en variables que ya son lo suficientemente densas.
    
- **Preparación de la Tubería**: Al limpiar estas columnas primero, garantizamos que las etiquetas críticas (como `genre`) y las características con alta integridad estén listas. Esto facilita que el siguiente paso de **imputación** se concentre únicamente en las columnas que realmente tienen un problema de datos masivo.
    

---

Para cerrar este primer paso de limpieza, transformaremos nuestro problema en uno de **clasificación binaria**. Muchos algoritmos funcionan mejor (o exclusivamente) con objetivos numéricos. Al convertir la columna "genre" en valores de 1 y 0, estamos preparando el terreno para que el modelo KNN pueda identificar qué patrones separan al "Rock" de cualquier otro estilo musical.

```python
# 1. Visualizar nulos iniciales (Paso 1)
print(music_df.isna().sum().sort_values())

# 2. Eliminar filas con nulos en columnas con < 5% de nulos (Paso 2)
music_df = music_df.dropna(subset=["genre", "popularity", "loudness", "liveness", "tempo"])

# 3. Convertir la columna 'genre' en una característica binaria
# Si es "Rock" asignamos 1, de lo contrario 0
music_df["genre"] = np.where(music_df["genre"] == "Rock", 1, 0)

# Verificación final de nulos y dimensiones
print(music_df.isna().sum().sort_values())
print("Shape of the `music_df`: {}".format(music_df.shape))
```

---

### Análisis de la Transformación Binaria con `np.where`

Como futuro **SysAdmin/DevOps**, apreciarás que la eficiencia de `numpy` es significativamente mayor que usar bucles `for` tradicionales. Aquí te explico la lógica:

- **La potencia de `np.where`**: Funciona de manera vectorizada, similar a un "IF" en Excel o un operador ternario en C. Evalúa una condición en toda la columna a la vez, lo que lo hace extremadamente rápido incluso en datasets de gran tamaño.
    
    - `np.where(condición, valor_si_se_cumple, valor_si_no)`
        
- **Simplificación del Objetivo**: Al pasar de múltiples géneros a simplemente "Rock vs. Otros", estamos reduciendo la complejidad del problema. Esto es muy común cuando el negocio solo está interesado en detectar un evento específico (ej. "Intrusión" vs. "Normal" en logs de red).
    
- **Estado Final del Dataset**: Tras estos tres pasos, has eliminado el ruido insignificante y has estandarizado la etiqueta objetivo. Notarás que la forma (_shape_) del DataFrame se ha reducido ligeramente debido al `dropna`, pero la calidad de los datos restantes es ahora mucho mayor para el entrenamiento.
    

> 💡 **Tip de Ingeniería**: En flujos de trabajo de **MLOps**, este tipo de transformaciones suelen ser el primer paso de un script de "Data Cleaning". Asegurarte de que el objetivo sea binario facilita mucho el cálculo de métricas posteriores como la precisión, el recall y la curva ROC que vimos anteriormente.
