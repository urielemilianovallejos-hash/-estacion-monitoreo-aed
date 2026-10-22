"""
Simulación de una estación de monitoreo de temperatura ambiente (Corrientes)
- 5 sensores
- 24 mediciones por sensor (una por hora durante un día)
- El sensor 5 sube su temperatura de a poco (deriva)
- Dos rachas de temperaturas anormales (> 40 °C) en posiciones fijas
- Archivo de salida: mediciones_temperatura.csv con las columnas: sensor, nro, valor
"""

import csv
import math
import random

random.seed(2026)  # semilla fija: así siempre se genera el mismo CSV

# ---------- Parámetros (se pueden cambiar fácilmente) ----------
CANT_SENSORES = 5        # cantidad de sensores
CANT_LECTURAS = 24       # lecturas por sensor: una por hora
TEMP_MEDIA = 25.0        # temperatura media del día en °C
AMPLITUD = 6.0           # cuánto sube y baja la temperatura durante el día (°C)
RUIDO = 0.3              # pequeña variación aleatoria de cada medición (°C)
DERIVA_SENSOR_5 = 0.15   # °C que suma el sensor 5 en cada hora (sube de a poco)

# Cada sensor tiene un pequeño desvío propio, como pasa con sensores reales
DESVIO_SENSOR = {1: 0.0, 2: 0.4, 3: -0.3, 4: 0.2, 5: 0.0}

# Rachas de temperaturas anormales (posiciones FIJAS para poder validar después):
# (sensor, nro de la primera medición de la racha, cantidad de mediciones seguidas)
RACHAS = [
    (2, 8, 5),    # sensor 2: mediciones 8, 9, 10, 11 y 12
    (4, 17, 6),   # sensor 4: mediciones 17, 18, 19, 20, 21 y 22
]
UMBRAL_ANOMALIA = 40.0   # las lecturas de las rachas siempre quedan por encima de este valor

# ---------- Generación de datos ----------
filas = []  # acá vamos guardando [sensor, nro, valor]

for sensor in range(1, CANT_SENSORES + 1):
    for nro in range(1, CANT_LECTURAS + 1):
        hora = nro - 1  # la lectura 1 es la hora 0 (medianoche), la 24 es la hora 23

        # Ciclo diario: función seno que da el máximo a las 15 h y el mínimo a las 3 h.
        ciclo = AMPLITUD * math.sin(2 * math.pi * (hora - 9) / 24)

        # Temperatura = media + ciclo del día + desvío del sensor + ruido pequeño
        valor = TEMP_MEDIA + ciclo + DESVIO_SENSOR[sensor] + random.gauss(0, RUIDO)

        # El sensor 5 se comporta distinto: va sumando una deriva a medida que pasan las horas
        if sensor == 5:
            valor += DERIVA_SENSOR_5 * hora

        # Inyección de anomalías: si esta lectura cae dentro de una racha,
        # se reemplaza por un valor anormal entre 41 y 45 °C (siempre > 40 °C)
        for (s_racha, inicio, longitud) in RACHAS:
            if sensor == s_racha and inicio <= nro < inicio + longitud:
                valor = UMBRAL_ANOMALIA + 1 + random.uniform(0, 4)

        filas.append([sensor, nro, round(valor, 1)])  # un decimal

# ---------- Guardar en CSV ----------
with open("mediciones_temperatura.csv", "w", newline="") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["sensor", "nro", "valor"])  # encabezado
    escritor.writerows(filas)                      # una línea por lectura

print(f"Listo: se guardaron {len(filas)} lecturas en mediciones_temperatura.csv")

# ---------- Tabla de anomalías inyectadas ("verdad conocida") ----------
print("\nAnomalías inyectadas:")
print("sensor | nro inicial | longitud | nros afectados")
for (s_racha, inicio, longitud) in RACHAS:
    afectados = list(range(inicio, inicio + longitud))
    print(f"{s_racha:6d} | {inicio:11d} | {longitud:8d} | {afectados}")
