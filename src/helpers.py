import json
from datetime import datetime
import constants as c


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


def guardar_respuesta(respuesta, columnas):
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


def generar_salida(resultado, busquedas_fallidas, raw):
    # Imprimir resultados por consola.
    # Puedes commentarlo si hay muchas direcciones que buscar.
    print("---------------------------------------------")
    print("Resultados:")
    print(resultado)

    # Guardar busquedas fallidas
    write_busquedas_fallidas(busquedas_fallidas)
    # Imprimir busquedas fallidas.
    print("---------------------------------------------")
    print("Busquedas sin encontrar (mirar archivo fallidas.txt):")
    for busqueda in busquedas_fallidas:
        print(busqueda)

    print("---------------------------------------------")
    print("Guardando " + c.NOMBRE_RESULTADO + "...")
    # Guardar los resultados.
    resultado.to_csv(c.NOMBRE_RESULTADO, sep=";", index=False)

    # Guardar respuestas de google.
    if c.DEBUG:
        print("Guardando " + c.DEBUG_FILE + "...")
        write_json(c.DEBUG_FILE, raw)

    print("Busqueda acabada! con {} fallos".format(len(busquedas_fallidas)))
