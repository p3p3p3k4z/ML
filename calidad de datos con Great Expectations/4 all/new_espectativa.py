import pandas as pd
import great_expectations as gx

# 1. SETUP: Contexto y Datos de Infraestructura
context = gx.get_context()
data = {
    "server_id": [101, 102, 103, 104],
    "hostname": ["SRV-DB-PROD", "SRV-WEB-DEV", "srv-cache-01", "BACKUP_NODE"],
    "uptime_days": [45, 120, 0, 300],
    "status": ["active", "active", "provisioning", "active"],
    "load_avg": [0.75, 0.45, 0.0, 0.10],
    "last_check": ["2026-02-15", "2026-02-20", None, "2026-01-01"]
}
df = pd.DataFrame(data)
batch = context.sources.add_pandas(name="sysadmin_source").add_dataframe_asset(name="servers").get_batch_definition_whole_dataframe("all_data").get_batch(batch_parameters={"dataframe": df})

# ---------------------------------------------------------
# 2. EXPECTATIONS BÁSICAS Y DE TIPO (Nivel de Fila)
# ---------------------------------------------------------
# Validamos que el ID sea numérico y no nulo
batch.validate(expect=gx.expectations.ExpectColumnValuesToNotBeNull(column="server_id"))
batch.validate(expect=gx.expectations.ExpectColumnValuesToBeOfType(column="server_id", type_="int"))

# ---------------------------------------------------------
# 3. EXPECTATIONS DE CADENAS (Regex y Longitud)
# ---------------------------------------------------------
# El hostname debe seguir el estándar: Tres letras-Función-Entorno (ej. SRV-DB-PROD)
# RegEx: 3 mayúsculas, guion, 2+ mayúsculas, guion, mayúsculas
hostname_regex = r"^[A-Z]{3}-[A-Z]{2,}-[A-Z]+$"
batch.validate(expect=gx.expectations.ExpectColumnValuesToMatchRegex(column="hostname", regex=hostname_regex))

# Longitud: El hostname no debe exceder los 15 caracteres para compatibilidad de red
batch.validate(expect=gx.expectations.ExpectColumnValueLengthsToBeLessThan(column="hostname", value=15))

# ---------------------------------------------------------
# 4. EXPECTATIONS NUMÉRICAS Y AGREGADAS
# ---------------------------------------------------------
# Rango: El load_avg debe estar entre 0.0 y 1.0 (Nivel de fila)
batch.validate(expect=gx.expectations.ExpectColumnValuesToBeBetween(column="load_avg", min_value=0.0, max_value=1.0))

# Agregado: Esperamos tener al menos 3 servidores distintos en este reporte
batch.validate(expect=gx.expectations.ExpectColumnUniqueValueCountToBeBetween(column="server_id", min_value=3))

# Agregado: La mediana del uptime_days debe ser mayor a 30 (indicador de estabilidad)
batch.validate(expect=gx.expectations.ExpectColumnMedianToBeBetween(column="uptime_days", min_value=30))

# ---------------------------------------------------------
# 5. EXPECTATIONS CONDICIONALES (Lógica de Negocio)
# ---------------------------------------------------------
# REGLA: Si el servidor está en 'provisioning', su load_avg DEBE ser 0.0
conditional_exp = gx.expectations.ExpectColumnValuesToBeInSet(
    column="load_avg",
    value_set={0.0},
    condition_parser="pandas",
    row_condition='status == "provisioning"'
)
res_cond = batch.validate(expect=conditional_exp)

# ---------------------------------------------------------
# 6. CAPACIDAD DE ANÁLISIS (Fechas)
# ---------------------------------------------------------
# Verificamos que 'last_check' sea una fecha válida si no es nula
batch.validate(expect=gx.expectations.ExpectColumnValuesToBeDateutilParseable(column="last_check"))

print(f"¿Infraestructura validada con éxito?: {res_cond.success}")
