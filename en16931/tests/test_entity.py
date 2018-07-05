import pytest

from en16931.entity import Entity
from en16931.postal_address import PostalAddress


class TestEntity:

    def test_initialization(self):
        e = Entity(name="Acme Inc.", tax_scheme="VAT",
                   tax_scheme_id="ES34626691F", country="ES",
                   party_legal_entity_id="ES34626691F",
                   registration_name="Acme INc.", mail="acme@acme.io",
                   endpoint="ES76281415Y", endpoint_scheme="ES:VAT",
                   address="easy street", postalzone="08080",
                   city="Barcelona")
        assert e.is_valid()
        assert e.tax_scheme == "VAT"
        assert e.tax_scheme_id == "ES34626691F"
        assert e.endpoint == "ES76281415Y"
        assert e.registration_name == "Acme INc."

    def test_unsuported_tax_scheme(self):
        e = Entity()
        with pytest.raises(ValueError):
            e.tax_scheme = "ASF"

    def test_not_apostal_address(self):
        e = Entity()
        with pytest.raises(TypeError):
            e.postal_address = "some address"

    def test_invalid_entity(self):
        e = Entity(name="Asdf Inc.")
        assert not e.is_valid()

    def test_valid_entity(self):
        e = Entity()
        e.name = "Acme Inc."
        e.tax_scheme = "VAT"
        e.tax_scheme_id = "ES34626691F"
        e.country = "ES"
        e.party_legal_entity_id = "ES34626691F"
        e.registration_name = "Acme INc."
        e.endpoint = "ES76281415Y"
        e.endpoint_scheme = "ES:VAT"
        p = PostalAddress(address="easy street", city_name="Barcelona",
                          postal_zone="08080", country="ES")
        e.postal_address = p
        assert e.is_valid()
        assert e.tax_scheme == "VAT"
        assert e.tax_scheme_id == "ES34626691F"
        assert e.endpoint == "ES76281415Y"
        assert e.registration_name == "Acme INc."
