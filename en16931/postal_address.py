"""
Class for representing a Postal Address
"""
class PostalAddress:
    """PostalAddress class

    It represents a postal address of an :class:`Entity`.
    """

    def __init__(self, address=None, address2=None, city_name=None,
                 postal_zone=None, country=None, province=None):
        """Initializes a PostalAddress.

        Parameters
        ----------
        address: string.
            An address.

        address2: string.
            Additional address details.

        city_name: string.
            The name of a city.

        postal_zone: string.
            A valid postal zone.

        country: string.
            A valid two letter country code.

        province: string.
            A valid province code.

        """
        self.address = address
        self.address2 = address2
        self.city_name = city_name
        self.postal_zone = postal_zone
        self.country = country
        self.province = province

    @property
    def country(self):
        """The country of the address
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of the address.
        """
        # TODO validate country in ISO3166-1:Alpha2 format
        self._country = country
    
    @property
    def province(self):
        """The province of the address
        """
        return self._province

    @province.setter
    def province(self, province):
        """Sets the country of the address.
        """
        # TODO validate country in ISO3166-1:Alpha2 format
        self._province = province
