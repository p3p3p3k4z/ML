# Average speed in km per hour
# 60 minutos en una hora / minutos por km = km por hora
avg_speed_hour = 60 / regression.coefficients[0]
print(avg_speed_hour)

# Average minutes on ground at OGG
# OGG es el nivel de referencia, por lo que su tiempo en tierra es simplemente el intercepto.
inter = regression.intercept
print(inter)

# Average minutes on ground at JFK
# JFK tiene índice 3 en 'features', que corresponde al índice 3 en los coeficientes.
# El tiempo total es el intercepto (referencia) + el coeficiente específico de JFK.
avg_ground_jfk = inter + regression.coefficients[3]
print(avg_ground_jfk)

# Average minutes on ground at LGA
# LGA tiene índice 4 en 'features', que corresponde al índice 4 en los coeficientes.
avg_ground_lga = inter + regression.coefficients[4]
print(avg_ground_lga)