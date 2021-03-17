import constants as c
from helpers import (buscar_locations)


def run(entrada, salida):
    buscar_locations(entrada, salida)


if __name__ == "__main__":
    # Verifica los parametros necesarios.
    if not c.GOOGLE_API or not c.INPUT_CSV or not c.OUTPUT_CSV:
        raise Exception(
            "Verifica la Configuración: GOOGLE_API, INPUT_CSV, OUTPUT_CSV")

    run(entrada=c.INPUT_CSV, salida=c.OUTPUT_CSV)
