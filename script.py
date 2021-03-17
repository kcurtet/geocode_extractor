#!/usr/bin/env python3
"""Import geocode data from google."""

import os
import pandas as pd
from geopy import geocoders
from dotenv import load_dotenv
from helpers import (generar_texto_busqueda, guardar_respuesta,
                     write_busquedas_fallidas, write_json)

# Cargar archivo .env
load_dotenv()

# La Clave API sacada de .env o entre ""
CLAVE_API = os.getenv("GOOGLE_API") or ""

# Nombre de archivos
NOMBRE_CSV = "direcciones.csv"
NOMBRE_RESULTADO = "resultado.csv"

# Columnas del csv para hacer la busqueda
COLUMNA_NOMBRE = "nombre"
COLUMNA_DIRECCION = "direccion"

# Idioma para Google Geocode API
LANGUAGE = "fr"

# Guardar las respuestas de google en DEBUG_FILE
DEBUG = True
DEBUG_FILE = 'google_debug.json'


# Verifica los parametros necesarios.
if not CLAVE_API or not NOMBRE_CSV or not NOMBRE_RESULTADO:
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
    datos_csv = pd.read_csv(NOMBRE_CSV, sep=";")  # sep es el sarador del csv

    # Datos para hacer la busqueda. (El orden es importante)
    hoteles_para_busqueda = datos_csv[
        [COLUMNA_DIRECCION, COLUMNA_NOMBRE]].values

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
        if respuesta is None:
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

    # Guardar busquedas fallidas
    write_busquedas_fallidas(busquedas_fallidas)
    # Imprimir busquedas fallidas.
    print("---------------------------------------------")
    print("Busquedas sin encontrar (mirar archivo fallidas.txt):")
    for busqueda in busquedas_fallidas:
        print(busqueda)

    print("---------------------------------------------")
    print("Guardando " + NOMBRE_RESULTADO + "...")
    # Guardar los resultados.
    datos_para_resultado.to_csv(NOMBRE_RESULTADO, sep=";", index=False)

    # Guardar respuestas de google.
    if DEBUG:
        print("Guardando " + DEBUG_FILE + "...")
        write_json(DEBUG_FILE, raw)

    print("Busqueda acabada! con {} fallos".format(len(busquedas_fallidas)))


if __name__ == "__main__":
    main()
