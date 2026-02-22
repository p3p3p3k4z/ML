import pandas as pd
import great_expectations as gx

# 1. SETUP: Contexto y Datos
# ---------------------------------------------------------
context = gx.get_context()
df = pd.DataFrame({"energy_kwh": [450, 480], "temp": [25, 26]})

# 2. GESTIÓN DE COMPONENTES: Añadir y Listar
# ---------------------------------------------------------
# Registramos un Data Source (Motor de ejecución)
ds = context.data_sources.add_pandas(name="main_source")
asset = ds.add_dataframe_asset(name="energy_asset")
batch_def = asset.add_batch_definition_whole_dataframe(name="full_batch")

# Registramos Suites
suite = context.suites.add(gx.ExpectationSuite(name="production_suite"))
new_suite = context.suites.add(gx.ExpectationSuite(name="archive_suite"))

# Listamos componentes para verificar el inventario
print(f"Suites registradas: {context.suites.all()}")
print(f"Fuentes de datos: {context.data_sources.all()}")

# 3. ACTUALIZAR EXPECTATION SUITES: Copiar, Eliminar y Editar
# ---------------------------------------------------------
# Definimos una Expectativa inicial
expectation = gx.expectations.ExpectTableColumnCountToEqual(value=20)

# A. Copiar una Expectation a otra Suite
exp_copy = expectation.copy()
exp_copy.id = None  # Limpiamos el ID para evitar colisiones
new_suite.add_expectation(exp_copy)

# B. Actualizar una Expectation (Mantenimiento Correctivo)
expectation.value = 2  # Corregimos el valor esperado
expectation.save()    # Persistimos el cambio en 'production_suite'

# C. Eliminar una Expectation
suite.remove_expectation(expectation)
suite.save()

# 4. IMPLEMENTAR VALIDATION DEFINITIONS Y CHECKPOINTS
# ---------------------------------------------------------
# Creamos el contrato de validación
val_def = gx.ValidationDefinition(
    data=batch_def,
    suite=new_suite,
    name="daily_validation_def"
)

# Creamos el Checkpoint (El orquestador de producción)
checkpoint = context.checkpoints.add(
    gx.Checkpoint(
        name="energy_checkpoint",
        validation_definitions=[val_def]
    )
)

# 5. GESTIÓN Y EJECUCIÓN DEL CHECKPOINT
# ---------------------------------------------------------
# Recuperamos un checkpoint específico por nombre
active_checkpoint = context.checkpoints.get(name="energy_checkpoint")

# Ejecutamos la validación formal
checkpoint_results = active_checkpoint.run(batch_parameters={"dataframe": df})

print(f"¿Validación exitosa?: {checkpoint_results.success}")

# 6. LIMPIEZA DE INFRAESTRUCTURA (SysAdmin Mode)
# ---------------------------------------------------------
# Eliminamos componentes obsoletos para mantener el sistema limpio
context.checkpoints.delete(name="energy_checkpoint")
print(f"Checkpoints restantes: {context.checkpoints.all()}")
