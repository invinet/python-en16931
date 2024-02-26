"""
Class representing an Entity.
"""

from en16931.bank_info import BankInfo
from en16931.postal_address import PostalAddress


class Entity:
    """Entity class.

    It represents a party involved in the trade described by the
    invoice, such as seller or buyer party.

    You can initialize an Entity with most of its attributes:

    >>> e = Entity(name="Acme Inc.", tax_scheme="VAT",
    ...            tax_scheme_id="ES34626691F", country="ES",
    ...            party_legal_entity_id="ES34626691F",
    ...            registration_name="Acme INc.", mail="acme@acme.io",
    ...            endpoint="ES76281415Y", endpoint_scheme="ES:VAT",
    ...            address="easy street", postalzone="08080",
    ...            province="Barcelona, city="Barcelona")

    Or you can build it step by step:

    >>> e.name = "Acme Inc."
    >>> e.tax_scheme = "VAT"
    >>> e.tax_scheme_id = "ES34626691F"
    >>> e.country = "ES"
    >>> e.party_legal_entity_id = "ES34626691F"
    >>> e.registration_name = "Acme INc."
    >>> e.endpoint = "ES76281415Y"
    >>> e.endpoint_scheme = "ES:VAT"
    >>> p = PostalAddress(address="easy street", city_name="Barcelona",
    ...                   postal_zone="08080", province="Barcelona", country="ES")
    >>> e.postal_address = p

    You can assign a :class:`PostalAddress` to its :meth:`postal_address`
    property. You can also associate a :class:`BankInfo` instance to an
    Entity in order to store relevant banking information for debit and
    transfer payments:

    >>> bank_info = BankInfo(iban="ES661234563156", bic="AAAABBCCDDD")
    >>> e.bank_info = bank_info
    >>> e.bank_info.iban
    "ES661234563156"

    An entity is valid if it has a name, a country, valid ids,
    valid taxscheme and endpoint, and has an address.

    >>> e.is_Valid()
    True

    """

    def __init__(self, name=None, tax_scheme=None, tax_scheme_id=None, country=None,
                 party_legal_entity_id=None, registration_name=None, mail=None,
                 endpoint=None, endpoint_scheme=None, postalzone=None, city=None,
                 address=None, address2=None, province=None):
        """Initialize an Entity.

        TODO formal definition of Entity.

        Parameters
        ----------
        name: string.
            The name of the Entity.

        tax_scheme: string.
            The tax scheme of the Entity.

        tax_scheme_id: string.
            The tax ID of the Entity.

        country: string.
            Two letter code for the country of the Entity.

        party_legal_entity_id: string.
            The party legal entity of the Entity.

        registration_name: string.
            The Registration name of the Entity.

        mail: string.
            The contact Email of the Entity.

        endpoint: string.
            A valid PEPPOL endpoint.

        endpoint_scheme: string.
            The scheme defining the endpoint.

        postalzone: string.
            The postalzone of the address of the Entity.

        city: string.
            The city of the address of the Entity.

        address: string.
            The address of the Entity.

        address2: string.
            Additional addres field.

        province: string.
            The province of the Entity.

        Notes
        -----
        An entity is valid if it has a name, a country, valid ids,
        valid taxscheme and endpoint, and has an address.

        """
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
        self.address2 = address2
        self.province = province
        self._postal_address = None
        self._bank_info = None

    @property
    def bank_info(self):
        """Property: a :class:`BankInfo` instance

        Parameters
        ----------
        bank_info: BankInfo instance
            a valid BankInfo instance.

        Raises
        ------
        TypeError
            If the parameter is not a BankInfo instance
        ValueError
            If the BankInfo instance is not valid

        """
        return self._bank_info

    @bank_info.setter
    def bank_info(self, bank_info):
        """Sets the BankInfor instance
        """
        if isinstance(bank_info, BankInfo):
            if bank_info.is_valid():
                self._bank_info = bank_info
            else:
                raise ValueError("Invalid BankInfo instance")
        else:
            raise TypeError('Expected a BankInfo instance')

    @property
    def postal_address(self):
        """Property: The PostalAddress of the Entity.

        See the :class:`PostalAddress` class.

        Parameters
        ----------
        address: PostalAddress object.
            A PostalAddress instance.

        Raises
        ------
        TypeError: if the input is not a PostalAddreess
            or a subclass.

        """
        if self._postal_address is not None:
            return self._postal_address
        elif self.postalzone is None or self.country is None:
            return None
        else:
            return PostalAddress(address=self.address, address2=self.address2,  
                                 city_name=self.city, postal_zone=self.postalzone,
                                 province=self.province, country=self.country)

    @postal_address.setter
    def postal_address(self, address):
        """Sets the PostalAddress of the Entity
        """
        if isinstance(address, PostalAddress):
            self._postal_address = address
        else:
            msg = "Expected a PostalAddress object but got a {}"
            raise TypeError(msg.format(type(address)))

    @property
    def name(self):
        """Property: The name of the Entity.

        Parameters
        ----------
        name: string.
            The name for the Entity.

        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of the Entity
        """
        self._name = name

    @property
    def tax_scheme(self):
        """Property: The tax scheme of the Entity.

        Parameters
        ----------
        scheme: string.
            The tax scheme used by the Entity.

        Raises
        ------
        ValueError: if the tax scheme is not valid.

        """
        return self._tax_scheme

    @tax_scheme.setter
    def tax_scheme(self, scheme):
        """Sets the tax scheme of the Entity.
        """
        supported_schemes = {None, "VAT"}
        if scheme not in supported_schemes:
            raise ValueError("Unsupported tax scheme %s" % scheme)
        self._tax_scheme = scheme

    @property
    def tax_scheme_id(self):
        """Property: The tax ID of the Entity.

        Parameters
        ----------
        tax_scheme_id: string.
            The tax ID of the Entity.

        """
        return self._tax_scheme_id

    @tax_scheme_id.setter
    def tax_scheme_id(self, tax_scheme_id):
        """Sets the tax ID of the Entity.
        """
        # TODO validate ID
        self._tax_scheme_id = tax_scheme_id

    @property
    def endpoint_scheme(self):
        """Property: The endpoint scheme of the Entity.

        Parameters
        ----------
        endpoint_scheme: string.
            The scheme defining the endpoint.

        """
        return self._endpoint_scheme

    @endpoint_scheme.setter
    def endpoint_scheme(self, scheme):
        """Sets the endpoint scheme of the Entity.
        """
        # TODO validate scheme
        self._endpoint_scheme = scheme

    @property
    def endpoint(self):
        """Property: The endpoint ID of the Entity.

        Parameters
        ----------
        endpoint: string.
            A valid PEPPOL endpoint.

        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """Sets the endpoint ID of the Entity
        """
        # TODO validate endpoint
        self._endpoint = endpoint

    @property
    def country(self):
        """Property: The country of the entity.

        Parameters
        ----------
        country: string.
            Two letter code for the country of the Entity.

        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of the entity.
        """
        # TODO validate country
        self._country = country

    @property
    def province(self):
        """Property: The province of the entity.

        Parameters
        ----------
        province: string.
            Code for the province of the Entity.

        """
        return self._province

    @province.setter
    def province(self, province):
        """Sets the country of the entity.
        """
        # TODO validate country
        self._province = province

    @property
    def party_legal_entity_id(self):
        """The party legal entity ID
        """
        return self._party_legal_entity_id

    @party_legal_entity_id.setter
    def party_legal_entity_id(self, party_legal_entity_id):
        """Sets the party legal entity ID.

        Parameters
        ----------
        party_legal_entity_id: string.
            Party legal entity ID

        """
        # TODO validate party_legal_entity_id
        self._party_legal_entity_id = party_legal_entity_id

    @property
    def registration_name(self):
        """The registration name of the Entity.
        """
        return self._registration_name

    @registration_name.setter
    def registration_name(self, registration_name):
        """Sets the registration name of the entity.

        Parameters
        ----------
        registration_name: string.
            The Registration name of the Entity.

        """
        # TODO validate registration_name
        self._registration_name = registration_name

    @property
    def mail(self):
        """The contact mail of the Entity.
        """
        return self._mail

    @mail.setter
    def mail(self, mail):
        """Sets the contact mail of the Entity.
        """
        # TODO validate mail
        self._mail = mail

    def is_valid(self):
        """Returns True if the Entity is valid.

        An entity is valid if it has a name, a country, valid ids,
        valid taxscheme and endpoint, and has an address.
        """
        has_name = self._name is not None
        has_country = self._country is not None
        has_ids = (self._party_legal_entity_id is not None) and (self._tax_scheme_id is not None)
        has_valid_taxscheme = self._tax_scheme is not None
        has_endpoint = self._endpoint is not None
        has_address = self.postal_address is not None
        return (has_name and has_country and has_ids and has_valid_taxscheme
                and has_endpoint and has_address)
