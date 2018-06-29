
class PostalAddress:

    def __init__(self, address=None, city_name=None,
                 postal_zone=None, country=None):
        self.address = address
        self.city_name = city_name
        self.postal_zone = postal_zone
        self.country = country

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        # TODO validate country in ISO3166-1:Alpha2 format
        self._country = country
