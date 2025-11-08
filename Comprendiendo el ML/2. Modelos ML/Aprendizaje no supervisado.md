A diferencia del aprendizaje supervisado, este enfoque utiliza datos de entrenamiento que **no tienen una columna objetivo** (no hay etiquetas). El modelo no recibe "orientación" sobre cuál es la respuesta correcta.

El objetivo principal es que el modelo **observe el conjunto de datos** por sí mismo e **intente buscar patrones**, relaciones o estructuras ocultas.

---
### 📦 Agrupamiento (Clustering)

- **Objetivo:** **Encontrar grupos** (clústeres) naturales dentro de un conjunto de datos.
    
- **Cómo funciona:** El algoritmo agrupa las observaciones **buscando similitudes** entre ellas. Los miembros de un mismo grupo son muy similares entre sí, pero muy diferentes a los miembros de otros grupos.
    
- **Ejemplo:** **Detectar imágenes** y agruparlas, ya sea **por color**, por el **origen** de la foto, o por el contenido.
    
- **Algoritmos Comunes:**
    
    - **K-Medias (K-Means):** Un algoritmo en el que se debe **especificar el número (K) de clústeres** que se quieren encontrar.
        
    - **DBSCAN:** Un algoritmo basado en densidad donde se debe **especificar qué constituye una agrupación** (qué tan cerca deben estar los puntos para considerarse "vecinos").
        

---

### ⚠️ Detección de Anomalías

- **Objetivo:** Identificar observaciones que son significativamente diferentes del resto; es decir, **detectar valores atípicos** (outliers).
    
- **Aplicaciones:**
    
    - Puede ser un paso de limpieza de datos para **eliminar valores atípicos** antes de otro análisis.
        
    - Es muy útil para **detectar errores** (ej. en la entrada de datos) o problemas (ej. transacciones fraudulentas, fallos en maquinaria).
        

---

### 🛒  Asociación

- **Objetivo:** Descubrir reglas o patrones sobre cómo ciertos **acontecimientos ocurren juntos**.
    
- **Cómo funciona:** Busca relaciones entre elementos en grandes conjuntos de datos.
    
- **Ejemplo Clásico (Análisis de cesta de mercado):** Encontrar **qué objetos se compran juntos** en un supermercado. El ejemplo más famoso es la regla "quien compra vino, también compra queso".