import constants as c


class LocationParser():
    _columns = c.COLUMNAS
    _row = ["No hay resultados" for _ in _columns]

    def __init__(self, name, location):
        self.name = name
        self._location = location

        if location is not None:
            self._row = self.gen_row()

    def get_component(self, component_name):
        if self._location is not None:
            address_components = self._location.raw['address_components']

            for component in address_components:
                if component_name in component['types']:
                    return component['long_name'], component['short_name']

        return "No hay resultados", "No hay resultados"

    def gen_row(self):
        name = self.name
        location = self._location
        return tuple([
            name, location.latitude, location.longitude, location.address]) + \
            self.get_component('country') + \
            self.get_component('administrative_area_level_1') + \
            self.get_component('administrative_area_level_2') + \
            self.get_component('locality') + \
            self.get_component('postal_code')[:-1] + \
            self.get_component('route')[:-1] + \
            self.get_component('street_number')[:-1] + \
            tuple([self.get_location_type()])

    def get_location_type(self):
        return self._location.raw['geometry']['location_type']

    def to_dict(self):
        return dict(zip(self._columns, self._row))

    def to_list(self):
        return list(self._row)
