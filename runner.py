import os
import pandas as pd
from geopy.geocoders import GoogleV3
from functools import partial
from location_parser import LocationParser
import constants as c


class Runner():
    address_table = pd.DataFrame([], columns=c.COLUMNAS)
    locations_table = pd.DataFrame([], columns=(c.COLUMNA_NOMBRE,
                                                c.COLUMNA_DIRECCION))

    def __init__(self, input_filename=c.CSV_ENTRADA, output_filename=c.CSV_SALIDA):
        if None or "" in (input_filename, output_filename):
            raise Exception("Se necesita los argumentos ENTRADA Y SALIDA")

        self.input_filename = input_filename
        self.output_filename = output_filename

        self.google = GoogleV3(api_key=c.GOOGLE_API)
        self.geocode = partial(self.google.geocode, language=c.LANGUAGE)

        if os.path.exists(input_filename):
            self.read_input()
        else:
            raise Exception("CSV_ENTRADA no existe")

    def read_input(self):
        """Read csv from input_name"""
        tmp = pd.read_csv(self.input_filename, sep=";")
        self.address_table = tmp[[c.COLUMNA_NOMBRE, c.COLUMNA_DIRECCION]]

    def save_output(self):
        """Save a csv to output_name"""
        self.locations_table.to_csv(self.output_filename, sep=";", index=False)

    def load_last_output(self):
        """Load las output and return the length"""
        self.locations_table = pd.read_csv(self.output_filename, sep=";")

    def add_row(self, row):
        self.locations_table = \
            self.locations_table.append(row, ignore_index=True)

    def start(self):
        if os.path.exists(self.output_filename):
            self.load_last_output()
            len_address = len(self.address_table)
            len_locations = len(self.locations_table)
            if len_address == len_locations:
                print(f"Direcciones guardadas {len_address}/{len_locations}")
                return
            else:
                last_idx = len(self.locations_table) - 1
        else:
            last_idx = -1

        for idx, address_row in enumerate(self.address_table.values):

            if idx <= last_idx:
                continue

            name, address = address_row

            print(f"Buscando: {name}\n{address}\n")
            query = f"{name}, {address}"
            location = self.geocode(query.encode())
            row = LocationParser(name, location).to_dict()
            self.add_row(row)

            if idx % 10 == 0:
                print('Guardando ultimos 10 resultados...\n')
                self.save_output()

        print('Guardando...')
        self.save_output()
        print('Busqueda finalizada!')
