#!/usr/bin/env python3
"""Import geocode data from google."""

import pandas as pd
from geopy import geocoders
import constants as c
from helpers import (guardar_respuesta, generar_salida, generar_texto_busqueda)

# Las variables ahora estan en constants.py

# Verifica los parametros necesarios.
if not c.CLAVE_API or not c.NOMBRE_CSV or not c.NOMBRE_RESULTADO:
    raise Exception(
        "Verifica la Configuración: CLAVE_API, NOMBRE_CSV, NOMBRE_RESULTADO")


def main():
    # Como no puedo guardar los datos directamente en el csv
    # necessito crear unas lista por cada COLUMNA que voy a
    # añadir al csv.
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
    raw = []

    # Guardar busquedas sin respuesta.
    busquedas_fallidas = []

    # Cargar el csv en una variable.
    datos_csv = pd.read_csv(c.NOMBRE_CSV, sep=";")  # sep es el sarador del csv

    # Datos para hacer la busqueda. (El orden es importante)
    hoteles_para_busqueda = datos_csv[
        [c.COLUMNA_DIRECCION, c.COLUMNA_NOMBRE]].values

    # Preparar el geocoder
    google = geocoders.GoogleV3(api_key=c.CLAVE_API)

    # Por cada hotel en la LISTA. ejecuta este codigo
    for fila_hotel in hoteles_para_busqueda:

        BUSQUEDA = generar_texto_busqueda(fila_hotel[0], fila_hotel[1])

        print("------------------------------------")
        print("Buscando:\n" + BUSQUEDA)

        # Ejecutar Busqueda.
        respuesta = google.geocode(BUSQUEDA, language=c.LANGUAGE)

        # Si la respuesta NO ha encontrado nada.
        if respuesta is None:
            busquedas_fallidas.append(BUSQUEDA)
            print("Outch... Sin Respuesta para:\n" + BUSQUEDA)

        guardar_respuesta(respuesta, columnas)

        if c.DEBUG:
            raw.append(respuesta.raw)

    # Agreagar columnas al csv.
    for key in columnas.keys():
        datos_csv[key] = columnas[key]

    # Filtrar resultados.
    columnas_a_exportar = list(columnas.keys())
    columnas_a_exportar.insert(0, c.COLUMNA_NOMBRE)
    resultado = datos_csv[columnas_a_exportar]

    generar_salida(resultado, busquedas_fallidas, raw)


if __name__ == "__main__":
    main()
