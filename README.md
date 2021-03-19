# Google Geocode API Extractor

Programa para leer direcciones de un csv y guardar los datos
devueltos por Google Geocode API en otro csv.

## Instalación

``` shell
pip install -r requirements.txt
# o
pip install pandas geopy
```


## Utilización

Primero hay que configurar las variables `GOOGLE_API`, `CSV_ENTRADA` y `CSV_SALIDA` en `constants.py`

Luego ejecutar el programa

``` shell
python run.py
```


# Variables

Variables en el archivo `constants.py`

`GOOGLE_API`: La API KEY de Google Geocode API.

`CSV_ENTRADA`: CSV con las direcciones para buscar.

`CSV_SALIDA`: CSV donde se guardaran los resultados.

`LANGUAGE`: Idioma respuestas google.

`COLUMNA_NOMBRE`: Nombre de la columna con el nombre del hotel.

`COLUMNA_DIRECCION`: Nombre de la columna con la dirección del hotel.
