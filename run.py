import constants as c
from helpers import buscar_geocodes


def run(entrada, salida):
    buscar_geocodes(entrada, salida)


if __name__ == "__main__":
    # Verifica los parametros necesarios.
    if not c.GOOGLE_API or not c.CSV_ENTRADA or not c.CSV_SALIDA:
        raise Exception(
            "Verifica la Configuración: GOOGLE_API, INPUT_CSV, OUTPUT_CSV")

    run(entrada=c.CSV_ENTRADA, salida=c.CSV_SALIDA)
