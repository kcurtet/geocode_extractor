#!/usr/bin/env python3
"""Import geocode data from google."""

import os
import json
from datetime import datetime
import pandas as pd
from geopy import geocoders
from dotenv import load_dotenv

load_dotenv()

CLAVE_API = os.getenv("GOOGLE_API") or ""

# Nombre del csv en la misma carpeta
# El csv necesita las columnas "hotel" y "direccion"
NOMBRE_CSV = "direcciones.csv"

# Archivo csv resultado. en la misma carpeta.
NOMBRE_RESULTADO = "resultado.csv"

# DEBUG: Para guardar respuestas de google en google_raw.json
DEBUG = True

if not CLAVE_API or not NOMBRE_CSV or not NOMBRE_RESULTADO:
    raise Exception("Verifica la Clave API o los nombre de archivos")

# Funcion de apoyo


def extraer_attributo(respuesta_raw, attributo, short=False):
    """Sacar el ATTRIBUTO de la respuesta de google."""
    address_components = respuesta_raw['address_components']

    for component in address_components:
        if attributo in component['types']:
            return component['short_name'] if short else component['long_name']
    return attributo + " no encontrado"

def generar_texto_busqueda(direccion, hotel):
    """Generar cadena de texto para la busqueda del geocoder"""
    return "{direccion} {hotel}".format(
        direccion=direccion.encode(),
        hotel=hotel.encode()
    )

def print_log(out, msg):
    """Imprimir la hora con un mensage"""
    out.write('[{}] [{}]:\n'.format(
        datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        msg.encode()))

def write_busquedas_fallidas(busquedas_fallidas=[]):
    """Escribe un archivo fallidas.txt con las busquedas que han fallado."""
    with open('fallidas.txt', 'a') as out:
        print_log(out, "Busquedas Fallidas")
        for busqueda in busquedas_fallidas:
            out.write(busqueda + "\n")

def write_json(name, data):
    """Escribir datos json en un archivo"""
    with open(name, 'a') as out:
        print_log(out, "Nueva Busqueda")
        json.dump(data, out, indent=4)


# --------------------
# Variables Globales
# --------------------

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
    'raw': []
}


def guardar_respuesta(respuesta=None):
    """Guardar respuesta google en el mapa columnas."""
    if respuesta is None:
      for key in columnas.keys():
          columnas[key].append("No hay respuesta.")
    else:
        columnas['latitud'].append(respuesta.latitude)

        columnas['longitud'].append(respuesta.longitude)

        columnas['address'].append(respuesta.address)

        columnas['pais'].append(extraer_attributo(
            respuesta.raw, "country"))

        columnas['pais_short'].append(extraer_attributo(
            respuesta.raw, "country", short=True))

        columnas['area_1'].append(extraer_attributo(
            respuesta.raw, "administrative_area_level_1"))

        columnas['area_1_short'].append(extraer_attributo(
            respuesta.raw, "administrative_area_level_1", short=True))

        columnas['area_2'].append(extraer_attributo(
            respuesta.raw, "administrative_area_level_2"))

        columnas['area_2_short'].append(extraer_attributo(
            respuesta.raw, "administrative_area_level_2", short=True))

        columnas['localidad'].append(extraer_attributo(
            respuesta.raw, "locality"))

        columnas['localidad_short'].append(extraer_attributo(
            respuesta.raw, "locality", short=True))

        columnas['calle'].append(extraer_attributo(
            respuesta.raw, "route"))

        columnas['numero_calle'].append(extraer_attributo(
            respuesta.raw, "street_number"))

        columnas['codigo_postal'].append(extraer_attributo(
            respuesta.raw, "postal_code"))

        columnas['location_type'].append(
            respuesta.raw['geometry']['location_type'])

        if DEBUG:
            columnas['raw'].append(respuesta.raw)


def main():
    # Datos para hacer la busqueda. (El orden es importante)
    hoteles_para_busqueda = datos_csv[["direccion", "nombre"]].values

    # Preparar el geocoder
    google = geocoders.GoogleV3(api_key=CLAVE_API)

    # Guardar busquedas con respuesta None
    busquedas_fallidas= []

    # Por cada hotel en la LISTA. ejecuta este codigo
    for fila_hotel in hoteles_para_busqueda:

        BUSQUEDA = generar_texto_busqueda(fila_hotel[0], fila_hotel[1])

        print("------------------------------------")
        print("Buscando:\n" + BUSQUEDA)

        # Ejecutar Busqueda.
        respuesta = google.geocode(BUSQUEDA)

        # Si la respuesta NO ha encontrado nada.
        if respuesta is not None:
            guardar_respuesta(respuesta)
        else:
            guardar_respuesta(None)
            busquedas_fallidas.append(BUSQUEDA)
            print("Outch... Sin Respuesta para:\n" + BUSQUEDA)

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
        write_json('google_debug.json', columnas['raw'])

if __name__ == "__main__":
    main()
