# Intercept (average minutes on ground)
# El intercepto representa el valor de la duración cuando la distancia es 0,
# lo que puede interpretarse como el tiempo promedio en tierra.
inter = regression.intercept
print(inter)

# Coefficients
# Los coeficientes indican cómo cambia la duración por cada unidad de cambio en los predictores.
coefs = regression.coefficients
print(coefs)

# Average minutes per km
# Extraemos el primer (y único, en este caso simple) coeficiente, que corresponde a 'km'.
# Este valor representa cuántos minutos aumenta la duración por cada km adicional de vuelo.
minutes_per_km = regression.coefficients[0]
print(minutes_per_km)

# Average speed in km per hour
# Si 'minutes_per_km' es minutos/km, su inverso es km/minuto.
# Para obtener km/hora, multiplicamos por 60 minutos/hora.
avg_speed = 60 / minutes_per_km
print(avg_speed)