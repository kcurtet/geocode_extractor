"""Helper functions."""
import os.path
from functools import partial
from geopy.geocoders import GoogleV3
import pandas as pd
from location_extractor import LocationExtractor
import constants as c


def add_row_to_dataframe(row, dataframe):
    return dataframe.append(row, ignore_index=True)


def read_csv(entrada):
    """Leer el csv de ENTRADA como pandas.DataFrame"""
    return pd.read_csv(entrada, sep=";")


def write_csv(datos, salida):
    """Escribir pandas.DataFrame en un csv SALIDA"""
    datos.to_csv(salida, sep=";", index=False)


def crear_data_frame_vacio(columnas=c.COLUMNAS):
    return pd.DataFrame([], columns=columnas)


def buscar_geocodes(entrada, salida):
    print('------------------------------------------------')
    print('Buscando nombres y direcciones en:', entrada)
    entrada_csv = read_csv(entrada)

    # filtrar columnas que no utilizamos
    datos_busqueda = entrada_csv[[c.COLUMNA_DIRECCION, c.COLUMNA_NOMBRE]]

    ultimos_resultados = 0
    resultados_google = crear_data_frame_vacio()

    if os.path.exists(salida):
        resultados_google = read_csv(salida)
        ultimos_resultados = len(resultados_google)

    # geopy Cliente para Google Geocode API
    google_client = GoogleV3(api_key=c.GOOGLE_API)
    geocode = partial(google_client.geocode, language=c.LANGUAGE)

    for idx, hotel in enumerate(datos_busqueda.values):

        if idx + 1 <= ultimos_resultados:
            continue

        busqueda = "{} {}".format(hotel[0], hotel[1])
        print('------------------------------------------------')
        print('Buscado datos para:', busqueda)

        location = geocode(busqueda)  # Geopy Location

        print('------------------------------------------------')
        print('Guardando respuesta:', busqueda)
        row = LocationExtractor(hotel[1], location).to_dict()
        resultados_google = add_row_to_dataframe(row, resultados_google)
        write_csv(resultados_google, salida)  # Save Results on each iteration.

    print('------------------------------------------------')
    print("Busqueda Finalizada!")
