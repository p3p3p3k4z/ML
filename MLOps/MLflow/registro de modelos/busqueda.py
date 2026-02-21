# =================================================================
# BÚSQUEDA AVANZADA EN EL MODEL REGISTRY (MLFLOW CLIENT)
# =================================================================

# 1. Definimos el filtro para encontrar modelos por prefijo.
# Usamos 'name LIKE' seguido del patrón con el comodín '%' para buscar 
# cualquier nombre que empiece con 'Insurance'.
insurance_filter_string = "name LIKE 'Insurance%'"

# 2. Buscamos modelos que coincidan con el prefijo 'Insurance'.
# Usamos el método search_registered_models del cliente de MLflow.
# Este método consulta el catálogo centralizado del Registro.
print(client.search_registered_models(filter_string=insurance_filter_string))

# 3. Definimos el filtro para excluir modelos específicos.
# Usamos 'name !=' para encontrar todos los modelos cuyo nombre exacto 
# no sea 'Insurance'.
not_insurance_filter_string = "name != 'Insurance'"

# 4. Buscamos modelos que no sean iguales al nombre 'Insurance'.
# Esto es útil para auditar modelos de otros departamentos o proyectos.
print(client.search_registered_models(filter_string=not_insurance_filter_string))

# Autodocumentación:
# El Model Registry permite este tipo de consultas SQL-like para gestionar 
# el ciclo de vida de forma eficiente entre múltiples colaboradores.
