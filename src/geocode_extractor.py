#!/usr/bin/env python3
"""Import geocode data from google."""

import pandas as pd
from geopy import geocoders
import constants as c
from helpers import (guardar_respuesta, generar_resultado, generar_salida)

# Las variables ahora estan en constants.py

# Verifica los parametros necesarios.
if not c.CLAVE_API or not c.NOMBRE_CSV or not c.NOMBRE_RESULTADO:
    raise Exception(
        "Verifica la Configuración: CLAVE_API, NOMBRE_CSV, NOMBRE_RESULTADO")


def main():
    """Inicia el programa."""

    # Columnas para guardar datos de google.
    columnas = {
        'latitud': [],
        'longitud': [],
        'address': [],
        'pais': [],
        'pais_short': [],
        'area_1': [],
        'area_1_short': [],
        'area_2': [],
        'area_2_short': [],
        'localidad': [],
        'localidad_short': [],
        'calle': [],
        'numero_calle': [],
        'codigo_postal': [],
        'location_type': [],
    }

    # Guardar respuestas google.
    respuestas_raw = []

    # Guardar busquedas sin respuesta.
    busquedas_fallidas = []

    # Leer csv.
    datos_csv = pd.read_csv(c.NOMBRE_CSV, sep=";")

    # Preparar el geocoder
    google = geocoders.GoogleV3(api_key=c.CLAVE_API)

    # Filtrar columnas para la busqueda. (El orden es importante)
    lista_de_hoteles = datos_csv[[c.COLUMNA_DIRECCION, c.COLUMNA_NOMBRE]]

    # Por cada hotel en la LISTA. ejecuta este codigo
    for hotel in lista_de_hoteles.values:

        # 0: direccion,  1: nombre
        busqueda = f"{hotel[0]} {hotel[1]}"
        print("------------------------------------")
        print("Buscando:\n" + busqueda)

        # Ejecutar Busqueda.
        respuesta = google.geocode(busqueda, language=c.LANGUAGE)

        # Si la respuesta NO ha encontrado nada.
        if respuesta is None:
            busquedas_fallidas.append(busqueda)
            print("Outch... Sin Respuesta para:\n" + busqueda)
        elif c.DEBUG:
            respuestas_raw.append(respuesta.raw)

        guardar_respuesta(respuesta, columnas)

    # Agreagar columnas al csv.
    for nombre_columna in columnas:
        datos_csv[nombre_columna] = columnas[nombre_columna]

    # Filtrar resultados.
    resultado = generar_resultado(datos_csv, columnas)

    generar_salida(resultado, busquedas_fallidas, respuestas_raw)


if __name__ == "__main__":
    main()
