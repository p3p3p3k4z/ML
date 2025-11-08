El Procesamiento de Lenguaje Natural (o NLP, por sus siglas en inglés) es un campo de la IA que da a las computadoras la **capacidad de comprender, interpretar y generar el significado del lenguaje humano**, tanto en texto como en voz.

El primer desafío es cómo convertir palabras, que los humanos entienden, en números, que las computadoras puedan procesar.

---

### Bolsa de Palabras (Bag-of-Words, BoW)

Este es un método clásico y simple para representar texto. En lugar de entender la gramática o el orden, simplemente implica **contar el número de veces que aparece cada palabra** única en un documento.

- **N-gramas:** Una variante es usar "n-gramas", que cuentan secuencias de 'n' palabras juntas (ej. 2-gramas como "casa roja" o "me gusta"), lo que captura un poco más de contexto que las palabras sueltas.
    
- **Limitaciones:** La principal desventaja es que **el recuento de palabras no nos ayuda a considerar sinónimos** (para BoW, "auto" y "coche" son dos cosas totalmente distintas) ni a entender el contexto real.
    

---

### Incrustaciones de Palabras (Word Embeddings)

Este es un enfoque moderno y mucho más poderoso. El objetivo es **crear "atributos" (un vector de números) que agrupen palabras similares** en un espacio matemático.

- **Significado Matemático:** Estos vectores capturan el significado semántico. Las palabras con significados parecidos (ej. "perro" y "gato") tendrán vectores numéricos similares y estarán "cerca" en este espacio.
    
- **Analogías:** La gran ventaja es que estos **atributos tienen un significado matemático**, lo que permite realizar "aritmética con palabras". El ejemplo más famoso es:
    

> king - man + woman = queen
> 
> (El vector de "rey" menos el de "hombre" más el de "mujer" resulta en un vector muy cercano al de "reina").

---

### Tareas y Aplicaciones Comunes

Una vez que las máquinas pueden "entender" el texto, pueden realizar tareas complejas.

#### Tareas Principales

- **Traducción de Idiomas:** Convertir texto de un idioma a otro de forma coherente.
    
- **Análisis de Sentimientos:** Determinar si un fragmento de texto (como un tuit o una reseña) es positivo, negativo o neutral.
    
- **Generación de Texto:** Crear texto nuevo y coherente (usado por _chatbots_ avanzados).
    

#### Aplicaciones Diarias

Estas tareas impulsan muchas herramientas que usamos a diario:

- **Traducción** automática.
    
- **Chatbots** para atención al cliente.
    
- **Asistentes** virtuales (como Siri, Alexa o Google Assistant).
    
- **Análisis de sentimientos** para marcas en redes sociales.
    
- Filtros de spam y correctores gramaticales.