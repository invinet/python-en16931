from datetime import datetime

from en16931.entity import Entity
from en16931.utils import parse_date


class Invoice:

    def __init__(self, invoice_id=None, currency="EUR"):
        self.invoice_id = invoice_id or 1
        self.currency = currency
        self._ubl_version_id = "2.1"
        self._customization_id = "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0"
        self._profile_id = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
        self._invoice_type_code = 380
        self._issue_date = None
        self._issue_date = None
        self._seller_party = None
        self._buyer_party = None
        self.lines = []

    @property
    def issue_date(self):
        return self._issue_date

    @issue_date.setter
    def issue_date(self, date):
        if isinstance(date, datetime):
            self._issue_date = date
        elif isinstance(date, str):
            self._issue_date = parse_date(date)
        else:
            raise ValueError("Unrecognized date")

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, date):
        if isinstance(date, datetime):
            self._due_date = date
        elif isinstance(date, str):
            self._due_date = parse_date(date)
        else:
            raise ValueError("Unrecognized date")

    @property
    def seller_party(self):
        return self._seller_party

    @seller_party.setter
    def seller_party(self, party):
        if isinstance(party, Entity):
            if party.is_valid():
                self._seller_party = party
            else:
                raise ValueError("Invalid Entity")
        else:
            raise TypeError("Expected an Entity object")

    @property
    def buyer_party(self):
        return self._buyer_party

    @buyer_party.setter
    def buyer_party(self, party):
        if isinstance(party, Entity):
            if party.is_valid():
                self._buyer_party = party
            else:
                raise ValueError("Invalid Entity")
        else:
            raise TypeError("Expected an Entity object")

    def add_line(self, line):
        self.lines.append(line)
