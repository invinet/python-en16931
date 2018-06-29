from en16931.postal_address import PostalAddress


class Entity:

    def __init__(self, name=None, tax_scheme=None, tax_scheme_id=None, country=None,
                 party_legal_entity_id=None, registration_name=None, mail=None,
                 endpoint=None, endpoint_scheme=None, postalzone=None, city=None,
                 address=None):
        self.name = name
        self.tax_scheme = tax_scheme
        self.tax_scheme_id = tax_scheme_id
        self.endpoint = endpoint
        self.endpoint_scheme = endpoint_scheme
        self.country = country
        self.party_legal_entity_id = party_legal_entity_id
        self.registration_name = registration_name
        self.mail = mail
        self.postalzone = postalzone
        self.city = city
        self.address = address
        self._postal_address = None

    @property
    def postal_address(self):
        if self._postal_address is not None:
            return self._postal_address
        elif self.postalzone is None or self.country is None:
            return None
        else:
            return PostalAddress(address=self.address, city_name=self.city,
                                 postal_zone=self.postalzone, country=self.country)

    @postal_address.setter
    def postal_address(self, address):
        if isinstance(address, PostalAddress):
            self._postal_address = address
        else:
            msg = "Expected a PostalAddress object but got a {}"
            raise TypeError(msg.format(type(address)))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def tax_scheme(self):
        return self._tax_scheme

    @tax_scheme.setter
    def tax_scheme(self, scheme):
        supported_schemes = {None, "VAT"}
        if scheme not in supported_schemes:
            raise ValueError("Unsupported tax scheme %s" % scheme)
        self._tax_scheme = scheme

    @property
    def tax_scheme_id(self):
        return self._tax_scheme_id

    @tax_scheme_id.setter
    def tax_scheme_id(self, tax_scheme_id):
        # TODO validate ID
        self._tax_scheme_id = tax_scheme_id

    @property
    def endpoint_scheme(self):
        return self._endpoint_scheme

    @endpoint_scheme.setter
    def endpoint_scheme(self, scheme):
        # TODO validate scheme
        self._endpoint_scheme = scheme

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        # TODO validate endpoint
        self._endpoint = endpoint

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        # TODO validate country
        self._country = country

    @property
    def party_legal_entity_id(self):
        return self._party_legal_entity_id

    @party_legal_entity_id.setter
    def party_legal_entity_id(self, party_legal_entity_id):
        # TODO validate party_legal_entity_id
        self._party_legal_entity_id = party_legal_entity_id

    @property
    def registration_name(self):
        return self._registration_name

    @registration_name.setter
    def registration_name(self, registration_name):
        # TODO validate registration_name
        self._registration_name = registration_name

    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self, mail):
        # TODO validate mail
        self._mail = mail

    def is_valid(self):
        has_name = self._name is not None
        has_country = self._country is not None
        has_ids = (self._party_legal_entity_id is not None) and (self._tax_scheme_id is not None)
        has_valid_taxscheme = self._tax_scheme is not None
        has_endpoint = self._endpoint is not None
        has_address = self.postal_address is not None
        return (has_name and has_country and has_ids and has_valid_taxscheme
                and has_endpoint and has_address)
