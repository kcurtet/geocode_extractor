import os
from dotenv import load_dotenv

# Cargar archivo .env
load_dotenv()

# La Clave API sacada de .env o entre ""
GOOGLE_API = os.getenv("GOOGLE_API") or ""

# Nombre de archivos
INPUT_CSV = "direcciones.csv"
OUTPUT_CSV = "resultado.csv"

# Columnas del csv para hacer la busqueda
COLUMNA_NOMBRE = "nombre"
COLUMNA_DIRECCION = "direccion"

# Idioma para Google Geocode API
LANGUAGE = "fr"

# Guardar las respuestas de google en DEBUG_FILE
DEBUG = True
DEBUG_FILE = 'google_debug.json'
