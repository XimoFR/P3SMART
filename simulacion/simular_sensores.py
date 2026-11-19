"""Simula lecturas de 3 tipos de sensores y las escribe en InfluxDB (base 'smartcity').

Measurements:
  temperatura_humedad  tags: sensor_id, zona      fields: temperatura, humedad
  co2                  tags: sensor_id, zona      fields: co2_ppm
  calidad_agua         tags: sensor_id, punto     fields: ph, turbidez, temperatura_agua

Uso: python simulacion/simular_sensores.py
"""
import random
from datetime import datetime, timedelta, timezone

from influxdb_client_3 import InfluxDBClient3, Point

HOST = "http://localhost:8181"
DATABASE = "smartcity"
TOKEN = "sin-auth"   # el servidor corre con --without-auth, pero el cliente exige un token

LECTURAS_POR_SENSOR = 24      # 24 lecturas ...
INTERVALO_MIN = 5             # ... una cada 5 minutos (últimas 2 horas)

# Sensores: (sensor_id, tag de ubicación)
SENSORES_TEMP = [("temp-001", "centro"), ("temp-002", "norte"), ("temp-003", "sur"),
                 ("temp-004", "este"), ("temp-005", "oeste")]
SENSORES_CO2 = [("co2-001", "centro"), ("co2-002", "norte"), ("co2-003", "sur")]
SENSORES_AGUA = [("agua-001", "rio"), ("agua-002", "deposito"), ("agua-003", "fuente")]


def punto_temperatura(sensor_id, zona, t):
    return (Point("temperatura_humedad")
            .tag("sensor_id", sensor_id).tag("zona", zona)
            .field("temperatura", round(random.uniform(15, 32), 1))
            .field("humedad", round(random.uniform(30, 80), 1))
            .time(t))


def punto_co2(sensor_id, zona, t):
    return (Point("co2")
            .tag("sensor_id", sensor_id).tag("zona", zona)
            .field("co2_ppm", round(random.uniform(400, 1200), 0))
            .time(t))


def punto_agua(sensor_id, punto, t):
    return (Point("calidad_agua")
            .tag("sensor_id", sensor_id).tag("punto", punto)
            .field("ph", round(random.uniform(6.5, 8.5), 2))
            .field("turbidez", round(random.uniform(0.1, 5.0), 2))
            .field("temperatura_agua", round(random.uniform(10, 24), 1))
            .time(t))


def generar_puntos():
    ahora = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    puntos = []
    for i in range(LECTURAS_POR_SENSOR):
        t = ahora - timedelta(minutes=INTERVALO_MIN * i)
        puntos += [punto_temperatura(s, z, t) for s, z in SENSORES_TEMP]
        puntos += [punto_co2(s, z, t) for s, z in SENSORES_CO2]
        puntos += [punto_agua(s, p, t) for s, p in SENSORES_AGUA]
    return puntos


if __name__ == "__main__":
    puntos = generar_puntos()
    with InfluxDBClient3(host=HOST, database=DATABASE, token=TOKEN) as cliente:
        cliente.write(record=puntos)
    print(f"Escritos {len(puntos)} puntos en '{DATABASE}' "
          f"({len(SENSORES_TEMP)} temp/humedad, {len(SENSORES_CO2)} co2, {len(SENSORES_AGUA)} agua).")
