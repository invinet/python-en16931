"""
Class for representing a Postal Address
"""
class PostalAddress:
    """PostalAddress class

    It represents a postal address of an :class:`Entity`.
    """

    def __init__(self, address=None, city_name=None,
                 postal_zone=None, country=None):
        """Initializes a PostalAddress.

        Parameters
        ----------
        address: string.
            An address.

        city_name: string.
            The name of a city.

        postal_zone: string.
            A valid postal zone.

        country: string.
            A valid two letter country code.

        """
        self.address = address
        self.city_name = city_name
        self.postal_zone = postal_zone
        self.country = country

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
