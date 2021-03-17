# Google Geocode API Extractor

Programa para leer direcciones de un csv y guardar los datos
devueltos por Google Geocode API en otro csv.

## Instalación

``` shell
pip install -r requirements.txt
# o
pip install pandas geopy python-dotenv
```


## Utilización

Primero hay que configurar las variables `GOOGLE_API`, `INPUT_CSV` y `OUTPUT_CSV` en `constants.py`

Luego ejecutar el programa

``` shell
python run.py
```

