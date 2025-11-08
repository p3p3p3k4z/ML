### Calidad de Datos

Esta es la limitación más fundamental. El principio clave es: **"con datos malos se producen resultados malos"** (conocido como _Garbage In, Garbage Out_).

- **No confiar ciegamente:** Nunca se debe **confiar en el modelo** por completo sin antes **ser consciente de los datos** con los que fue entrenado.
    
- **Control de Calidad:** Es esencial aplicar un riguroso control de calidad a los datos antes de usarlos. Esto incluye:
    
    - **Análisis de datos** exploratorio.
        
    - **Revisión de datos atípicos** (outliers).
        
    - Mantener un nivel de **sospecha** saludable sobre la fuente y precisión de los datos.
        
    - Tener una buena **documentación** del origen y las transformaciones de los datos.
        

---

### Explicabilidad

Muchos modelos de ML, especialmente los de _Deep Learning_, funcionan como una **"caja negra"** (_black box_): dan una respuesta correcta, pero no podemos saber _cómo_ o _por qué_ llegaron a ella.

- **IA Explicable (XAI):** Es un campo emergente que busca crear modelos con **transparencia** para **aumentar la confianza, la claridad y la comprensión**.
    
- **Ejemplo de XAI:** Un modelo de "caja negra" podría predecir si un paciente tendrá diabetes con un 90% de exactitud. Un modelo de **IA explicable** podría predecir lo mismo _y además_ explicar **por qué ocurre** (ej. "debido a los altos niveles de glucosa y el índice de masa corporal").
    

La explicabilidad es crucial para varios **casos prácticos**:

- **Adopción empresarial:** Para que los líderes confíen en las decisiones del modelo.
    
- **Supervisión normativa:** Para cumplir con leyes que exigen saber cómo se toma una decisión (ej. por qué se rechazó un crédito).
    
- **Minimización del sesgo:** Para asegurar que el modelo no esté discriminando basándose en atributos sensibles (género, raza, etc.).