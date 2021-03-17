"""Helper functions."""
import os.path
from geopy import geocoders
import pandas as pd
import constants as c
from datetime import datetime


def extraer_attributo(respuesta, attributo, short=False):
    """Sacar el ATTRIBUTO de la respuesta de google."""
    address_components = respuesta.raw['address_components']

    for component in address_components:
        if attributo in component['types']:
            return component['short_name'] if short else component['long_name']
    return attributo + " no encontrado"


def leer_entrada(entrada, columnas):
    data = pd.read_csv(entrada, sep=";")
    print("---------------------------------------------------------")
    print("Leyendo archivo " + entrada)
    return data[columnas].values


def generar_busqueda(hotel):
    return f"{hotel[0]} {hotel[1]}"


def buscar_resultados(busqueda, api_key, language):
    google = geocoders.GoogleV3(api_key=api_key)
    print("---------------------------------------------------------")
    print("Buscado resultados para:\n" + busqueda)
    return google.geocode(busqueda.encode(), language=language)


def extraer_valor_para(key, respuesta):
    switcher = {
        'latitud': respuesta.latitude,
        'longitud': respuesta.longitude,
        'address': respuesta.address,
        'pais': extraer_attributo(respuesta, "country"),
        'pais_short': extraer_attributo(respuesta, "country", short=True),
        'area_1': extraer_attributo(
            respuesta, "administrative_area_level_1"),
        'area_1_short': extraer_attributo(
            respuesta, "administrative_area_level_1", short=True),
        'area_2': extraer_attributo(
            respuesta, "administrative_area_level_2"),
        'area_2_short': extraer_attributo(
            respuesta, "administrative_area_level_2", short=True),
        'localidad': extraer_attributo(respuesta, "locality"),
        'localidad_short': extraer_attributo(
            respuesta, "locality", short=True),
        'calle': extraer_attributo(respuesta, "route"),
        'numero_calle': extraer_attributo(respuesta, "street_number"),
        'codigo_postal': extraer_attributo(respuesta, "postal_code"),
        'location_type': respuesta.raw['geometry']['location_type'],
    }

    return switcher[key]


def extraer_datos_google(respuesta):

    COLUMNAS = ['latitud', 'longitud', 'pais', 'pais_short',
                'area_1', 'area_1_short', 'area_2', 'area_2_short',
                'localidad', 'localidad_short', 'calle', 'numero_calle',
                'codigo_postal', 'location_type']

    result = {}

    if respuesta is None:
        for key in COLUMNAS:
            result[key] = ["No Hay resultado"]
    else:
        for key in COLUMNAS:
            result[key] = [extraer_valor_para(key, respuesta)]

    return pd.DataFrame(result, columns=COLUMNAS)


def guardar_resupuesta(nombre, respuesta, salida):
    fila = extraer_datos_google(respuesta)
    fila = pd.DataFrame({'nombre': [nombre]}).join(fila)
    if os.path.isfile(salida):
        tmp = pd.read_csv(salida, sep=";")
        tmp.append(fila, ignore_index=True).to_csv(salida, sep=";", index=False)
    else:
        fila.to_csv(salida, sep=";", index=False)

    print("---------------------------------------------------------")
    print("Gardando resultado " + nombre)


def guardar_fallidas(fallidas):
    with open('fallidas.txt', 'a') as f:
        time = datetime.now().strftime("%Y/%m/%d %HH:%MM:%s")
        f.write(f"{time} [Respuestas Fallidas]:\n")
        for busqueda in fallidas:
            f.write(busqueda + "\n")


def buscar_locations(entrada, salida):
    lista_hoteles = leer_entrada(entrada, columnas=[
        c.COLUMNA_DIRECCION, c.COLUMNA_NOMBRE
    ])

    fallidas = []

    try:
        output = pd.read_csv(salida, sep=";")
        ultimo_resultado = len(output)
    except FileNotFoundError:
        ultimo_resultado = 0

    for idx, hotel in enumerate(lista_hoteles):

        if idx < ultimo_resultado:
            continue

        busqueda = generar_busqueda(hotel)

        respuesta = buscar_resultados(busqueda,
                                      c.GOOGLE_API, language=c.LANGUAGE)

        if respuesta is None:
            fallidas.append(busqueda)

        nombre = hotel[1]
        guardar_resupuesta(nombre, respuesta, salida)

    guardar_fallidas(fallidas)

    print("---------------------------------------------------------")
    print('Busqueda Terminada!')
    print('Busquedas Totales:', idx + 1 - ultimo_resultado)
    print('Fallidas:', len(fallidas))
