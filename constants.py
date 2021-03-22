import os

# La Clave API
GOOGLE_API = os.environ.get('API_KEY') or ""

# Nombre de archivos
CSV_ENTRADA = "direcciones.csv"
CSV_SALIDA = "resultado.csv"

# Columnas del csv para hacer la busqueda
COLUMNA_NOMBRE = "nombre"
COLUMNA_DIRECCION = "direccion"

# Idioma para Google Geocode API
LANGUAGE = "fr"

# Columnas que guardara de google. (Avisame para cambiarlas.)
COLUMNAS = [
    'nombre', 'latitud', 'longitud', 'address', 'pais', 'pais_short',
    'area_1', 'area_1_short', 'area_2', 'area_2_short',
    'localidad', 'localidad_short', 'codigo_postal',
    'calle', 'numero_calle', 'location_type'
]
