import os
from dotenv import load_dotenv

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
