from typing import Iterable, List, Dict


class LocationExtractor():
    def __init__(self, name: str, location):
        self.name = name
        self._location = location
        self._columnas = [
            'nombre', 'latitud', 'longitud', 'address', 'pais', 'pais_short',
            'area_1', 'area_1_short', 'area_2', 'area_2_short',
            'localidad', 'localidad_short', 'codigo_postal',
            'calle', 'numero_calle', 'location_type'
        ]

        if self._location is not None:
            self.address: str = location.address
            self.latitude: float = location.latitude
            self.longitude: float = location.longitude
            self.raw: Dict = location.raw
            self.address_components: Iterable = \
                location.raw['address_components']
            self.init_components()

    def init_components(self):
        self.country, self.country_short = \
            self.get_component('country')
        self.area_1, self.area_1_short = \
            self.get_component('administrative_area_level_1')
        self.area_2, self.area_2_short = \
            self.get_component('administrative_area_level_2')
        self.locality, self.locality_short = \
            self.get_component('locality')
        self.postal_code = self.get_component('postal_code')[0]
        self.route = self.get_component('route')[0]
        self.street_number = self.get_component('street_number')[0]
        self.location_type = self.get_location_type()

    def get_component(self, component_name: str):
        if self.address_components is None:
            return "No hay resultados", "No hay resultados"
        for component in self.address_components:
            if component_name in component['types']:
                return component['long_name'], component['short_name']

    def get_location_type(self):
        return str(self.raw['geometry']['location_type']),

    def to_dict(self) -> Dict:
        return dict(zip(self._columnas, self.to_list()))

    def to_list(self) -> List:
        defaults = ['No hay resultados' for i in range(len(self._columnas))]

        if self._location is None:
            return defaults

        return [
            self.name, self.latitude, self.longitude, self.address, self.country, self.country_short,
            self.area_1, self.area_1_short, self.area_2, self.area_2_short, self.locality, self.locality_short,
            self.postal_code, self.route, self.street_number, self.location_type
        ]
