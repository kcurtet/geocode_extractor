#!/usr/bin/env python3
"""Import geocode data from google."""

import os
import pandas as pd
from geopy import geocoders
from dotenv import load_dotenv
from helpers import (generar_texto_busqueda, guardar_respuesta,
                     write_busquedas_fallidas, write_json)

load_dotenv()

CLAVE_API = os.getenv("GOOGLE_API") or ""

# Nombre del csv en la misma carpeta
# El csv necesita las columnas "hotel" y "direccion"
NOMBRE_CSV = "direcciones.csv"

# Archivo csv resultado. en la misma carpeta.
NOMBRE_RESULTADO = "resultado.csv"

# Lenguage Google Api
LANGUAGE = "fr"

# DEBUG: Para guardar respuestas de google en google_raw.json
DEBUG = True

if not CLAVE_API or not NOMBRE_CSV or not NOMBRE_RESULTADO:
    raise Exception("Verifica la Clave API o los nombre de archivos")

# Cargar el csv en una variable.
datos_csv = pd.read_csv(NOMBRE_CSV, sep=";")  # sep es el sarador del csv

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


def main():
    # Datos para hacer la busqueda. (El orden es importante)
    hoteles_para_busqueda = datos_csv[["direccion", "nombre"]].values

    # Guardar respuestas google.
    raw = []

    # Guardar busquedas sin respuesta.
    busquedas_fallidas = []

    # Preparar el geocoder
    google = geocoders.GoogleV3(api_key=CLAVE_API)

    # Por cada hotel en la LISTA. ejecuta este codigo
    for fila_hotel in hoteles_para_busqueda:

        BUSQUEDA = generar_texto_busqueda(fila_hotel[0], fila_hotel[1])

        print("------------------------------------")
        print("Buscando:\n" + BUSQUEDA)

        # Ejecutar Busqueda.
        respuesta = google.geocode(BUSQUEDA, language=LANGUAGE)

        # Si la respuesta NO ha encontrado nada.
        if respuesta is not None:
            busquedas_fallidas.append(BUSQUEDA)
            print("Outch... Sin Respuesta para:\n" + BUSQUEDA)

        guardar_respuesta(respuesta, columnas)

        if DEBUG:
            raw.append(respuesta.raw)

    # Agreagar columnas al csv.
    for key in columnas.keys():
        datos_csv[key] = columnas[key]

    # Lista de columnas prara darle a pandas
    columnas_a_exportar = list(columnas.keys())
    columnas_a_exportar.insert(0, "nombre")

    # En los resultados solo queremos las columnas nuevas.
    # con el nombre de cada hotel
    datos_para_resultado = datos_csv[columnas_a_exportar]

    # Imprimir resultados por consola.
    # Puedes commentarlo si hay muchas direcciones que buscar.
    print("---------------------------------------------")
    print("Resultados:")
    print(datos_para_resultado)

    # Imprimir busquedas fallidas.
    print("---------------------------------------------")
    print("Busquedas sin encontrar (mirar archivo fallidas.txt):")
    for busqueda in busquedas_fallidas:
        print(busqueda)

    # Guardar los resultados.
    datos_para_resultado.to_csv(NOMBRE_RESULTADO, sep=";", index=False)
    # Guardar busquedas fallidas
    write_busquedas_fallidas(busquedas_fallidas)
    # Guardar respuestas de google.
    if DEBUG:
        write_json('google_debug.json', raw)


if __name__ == "__main__":
    main()
