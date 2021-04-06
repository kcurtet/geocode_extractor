import constants as c
from runner import Runner
from geopy.exc import ConfigurationError

DEBUG = True


def main(entrada, salida):
    Runner(entrada, salida).start()


if __name__ == "__main__":
    # Verifica los parametros necesarios.
    try:
        main(entrada=c.CSV_ENTRADA, salida=c.CSV_SALIDA)
    except ConfigurationError as e:
        print("Error: GOOGLE_API no es valido")
        print(e)
    except Exception as e:
        if DEBUG:
            raise e
        else:
            print("Error Inesperado:", e)
