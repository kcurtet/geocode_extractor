"""Helper functions."""
import os.path
from geopy import geocoders
import pandas as pd
import constants as c


def pedir_google_geocode(cliente, busqueda):
    try:
        return cliente.geocode(busqueda, language=c.LANGUAGE)
    except Exception:
        raise Exception("Error Geopy: No se puede conectar con google.")


def get_address_component(respuesta, attributo, short=False):
    """Sacar el ATTRIBUTO de la respuesta de google."""
    address_components = respuesta.raw['address_components']

    for component in address_components:
        if attributo in component['types']:
            return component['short_name'] if short else component['long_name']

    return attributo + " no encontrado"


def extraer_datos_google(columna, respuesta):
    switcher = {
        'latitud': respuesta.latitude,
        'longitud': respuesta.longitude,
        'address': respuesta.address,
        'pais': get_address_component(respuesta, "country"),
        'pais_short': get_address_component(respuesta, "country", short=True),
        'area_1': get_address_component(
            respuesta, "administrative_area_level_1"),
        'area_1_short': get_address_component(
            respuesta, "administrative_area_level_1", short=True),
        'area_2': get_address_component(
            respuesta, "administrative_area_level_2"),
        'area_2_short': get_address_component(
            respuesta, "administrative_area_level_2", short=True),
        'localidad': get_address_component(respuesta, "locality"),
        'localidad_short': get_address_component(
            respuesta, "locality", short=True),
        'calle': get_address_component(respuesta, "route"),
        'numero_calle': get_address_component(respuesta, "street_number"),
        'codigo_postal': get_address_component(respuesta, "postal_code"),
        'location_type': respuesta.raw['geometry']['location_type'],
    }

    return switcher.get(columna, 'Columna sin definir')


def generar_fila_csv(respuesta):
    columnas = ['latitud', 'longitud', 'pais', 'pais_short',
                'area_1', 'area_1_short', 'area_2', 'area_2_short',
                'localidad', 'localidad_short', 'calle', 'numero_calle',
                'codigo_postal', 'location_type']

    datos = []
    if respuesta is None:
        for columna in columnas:
            datos.append("Sin repuesta de google")
    else:
        for columna in columnas:
            datos.append(extraer_datos_google(columna, respuesta))

    return pd.DataFrame([datos], columns=columnas)


def agregar_fila(datos, fila):
    return datos.append(fila, ignore_index=True)


def leer_csv_entrada(entrada):
    return pd.read_csv(entrada, sep=";")


def escribir_csv_salida(datos, salida):
    datos.to_csv(salida, sep=";", index=False)


def buscar_geocodes(entrada, salida):
    print('------------------------------------------------')
    print('Buscando nombres y direcciones en:', entrada)
    entrada_csv = leer_csv_entrada(entrada)

    # filtrar columnas que no utilizamos
    datos = entrada_csv[[c.COLUMNA_DIRECCION, c.COLUMNA_NOMBRE]]

    ultimos_resultados = 0
    columnas_con_nombre = [c.COLUMNA_NOMBRE] + c.COLUMNAS
    datos_para_guardar = pd.DataFrame([], columns=columnas_con_nombre)

    if os.path.exists(salida):
        datos_salida = leer_csv_entrada(salida)
        ultimos_resultados = len(datos_salida)
        datos_para_guardar = datos_salida

    # geopy Cliente para Google Geocode API
    clienteGoogle = geocoders.GoogleV3(api_key=c.GOOGLE_API)

    for idx, fila in enumerate(datos.values):

        if idx + 1 <= ultimos_resultados:
            continue

        busqueda = "{} {}".format(fila[0], fila[1])
        print('------------------------------------------------')
        print('Buscado datos para:', busqueda)
        respuesta = pedir_google_geocode(clienteGoogle, busqueda.encode())
        nueva_fila = generar_fila_csv(respuesta)
        nueva_fila.insert(0, c.COLUMNA_NOMBRE, fila[1])
        datos_para_guardar = agregar_fila(datos_para_guardar, nueva_fila)
        print('------------------------------------------------')
        print('Guardando respuesta:', busqueda)
        escribir_csv_salida(datos_para_guardar, salida)

    print('------------------------------------------------')
    print("Busqueda Finalizada!")
