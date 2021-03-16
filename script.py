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


# --------------------
# Variables Globales
# --------------------

# Cargar el csv en una variable.
datos_csv = pd.read_csv(NOMBRE_CSV, sep=";")  # sep es el sarador del csv

# Extraer los campos del csv para la busqueda.
#
# Creamos una LISTA de los hoteles con las
# COLUMNAS (0:direccion, 1:nombre).
#
# [["columna1", "columna2"]] para filtrar las COLUMNAS
# .values para sacar una LISTA con los datos.
hoteles_para_busqueda = datos_csv[["direccion", "nombre"]].values

# Como no puedo guardar los datos directamente en el csv
# necessito crear unas lista por cada COLUMNA que voy a
# añadir al csv.

columna_latitud = []
columna_longitud = []
columna_address = []
columna_pais = []
columna_pais_short = []
columna_area_1 = []
columna_area_1_short = []
columna_area_2 = []
columna_area_2_short = []
columna_localidad = []
columna_localidad_short = []
columna_calle = []
columna_numero_calle = []
columna_location_type = []
columna_postal = []

# lista para respuestas de google. solo si DEBUG es True.
if DEBUG:
    google_raw = []

# --------------------
# Hacer las busquedas.
# --------------------

# Iniciar el geocoder para google
google = geocoders.GoogleV3(api_key=CLAVE_API)

# Por cada hotel en la LISTA. ejecuta este codigo
for fila_hotel in hoteles_para_busqueda:

    # Cadena de texto con la direccion y hotel para
    # darle a geocoder.
    #
    # .format: remplaza los {variable} con la variable
    # del mismo nombre que le pases.
    # .encode: para quitar symbolos que nos son utf8
    BUSQUEDA = "{direccion} {hotel}".format(
        direccion=fila_hotel[0].encode(),  # 0 = direccion
        hotel=fila_hotel[1].encode()       # 1 = nombre hotel
    )

    # Imprimir mensage en consola para ver las busquedas.
    print("------------------------------------")
    print("Buscando: " + BUSQUEDA)

    # importar geocoder
    respuesta = google.geocode(BUSQUEDA)

    # Si la respuesta NO ha encontrado nada.
    if respuesta is None:
        ##################################################
        # Rellenamos la siguiente fila. con "No hay resultado"
        ##################################################
        columnas = [
            columna_address, columna_postal, columna_latitud, columna_longitud,
            columna_pais, columna_pais_short, columna_localidad,
            columna_localidad_short, columna_calle, columna_numero_calle,
            columna_area_1, columna_area_1_short, columna_location_type,
            columna_area_2, columna_area_2_short
        ]

        # Por cada columna rellena con "No hay resultado de google."
        for columna in columnas:
            columna.append("No hay resultado de google.")

        # Imprimir información sobre resultado no encontrado.
        print("Error: No hay resultados para: " + BUSQUEDA
              + "\nConsejo: Verifica la api"
              + "\nConsejo: Puede ser el nombre o la direccion"
              + "\nConsejo: Consulta con Kevin")

    # Si la respuesta SI ha sido un exito.
    else:
        ##################################################
        # Guardamos la siguiente fila.
        ##################################################
        columna_latitud.append(respuesta.latitude)
        columna_longitud.append(respuesta.longitude)
        columna_address.append(respuesta.address)

        columna_pais.append(extraer_attributo(
            respuesta.raw, "country"))

        columna_pais_short.append(extraer_attributo(
            respuesta.raw, "country", short=True))

        columna_area_1.append(extraer_attributo(
            respuesta.raw, "administrative_area_level_1"))

        columna_area_1_short.append(extraer_attributo(
            respuesta.raw, "administrative_area_level_1", short=True))

        columna_area_2.append(extraer_attributo(
            respuesta.raw, "administrative_area_level_2"))

        columna_area_2_short.append(extraer_attributo(
            respuesta.raw, "administrative_area_level_2", short=True))

        columna_localidad.append(extraer_attributo(
            respuesta.raw, "locality"))

        columna_localidad_short.append(extraer_attributo(
            respuesta.raw, "locality", short=True))

        columna_calle.append(extraer_attributo(
            respuesta.raw, "route"))

        columna_numero_calle.append(extraer_attributo(
            respuesta.raw, "street_number"))

        columna_postal.append(extraer_attributo(
            respuesta.raw, "postal_code"))

        columna_location_type.append(
            respuesta.raw['geometry']['location_type'])

        if DEBUG:
            google_raw.append(respuesta.raw)

###############################################
# Agregar COLUMNAS creadas al CSV en memoria.
###############################################

datos_csv["latitud"] = columna_latitud
datos_csv["longitud"] = columna_longitud
datos_csv["address"] = columna_address
datos_csv["pais"] = columna_pais
datos_csv["pais_short"] = columna_pais_short
datos_csv["area_1"] = columna_area_1
datos_csv["area_1_short"] = columna_area_1_short
datos_csv["area_2"] = columna_area_2
datos_csv["area_2_short"] = columna_area_2_short
datos_csv["localidad"] = columna_localidad
datos_csv["localidad_short"] = columna_localidad_short
datos_csv["calle"] = columna_calle
datos_csv["numero_calle"] = columna_numero_calle
datos_csv["codigo_postal"] = columna_postal
datos_csv["location_type"] = columna_location_type

###############################################
# Guardar Resultados.
###############################################

# Crear una variable con las COLUMNAS del csv que queremos guardar
datos_para_resultado = datos_csv[
    ["nombre", "latitud", "longitud", "address",
     "pais", "pais_short", "area_1", "area_1_short",
     "area_2", "area_2_short", "localidad",
     "calle", "numero_calle", "codigo_postal", "location_type"]]


# Imprimir resultados por consola.
# Puedes commentarlo si hay muchas direcciones que buscar.
print(datos_para_resultado)

# Guardar los resultados en csv
datos_para_resultado.to_csv(NOMBRE_RESULTADO, sep=";", index=False)

# Guardar respuestas de google. en otro archivo. si DEBUG es True
if DEBUG:
    with open('google_raw.json', 'a') as out:
        out.write('[{}] [Nueva Busqueda]:\n'.format(
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
        json.dump(google_raw, out, indent=4)
