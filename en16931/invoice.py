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
            msg = "Expected an Entity object but got a {}"
            raise TypeError(msg.format(type(party)))

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
            msg = "Expected an Entity object but got a {}"
            raise TypeError(msg.format(type(party)))

    def add_line(self, line):
        self.lines.append(line)

    def add_lines_from(self, container):
        self.lines.extend(container)

    @property
    def unique_taxes(self):
        return {line.tax for line in self.lines}

    def lines_with_taxes(self, tax_type=None):
        for line in self.lines:
            if line.has_tax(tax_type):
                yield line

    def tax_amount(self, tax_type=None):
        if tax_type is None:
            taxes = self.unique_taxes
        else:
            taxes = {tax_type}
        result = (round(self.taxable_base(tax_type=tax) * tax.percent, 2) for tax in taxes)
        return round(sum(result), 2)

    def taxable_base(self, tax_type=None):
        # TODO global discount
        allowance_total_amount = 0
        return self.gross_subtotal(tax_type=tax_type) - allowance_total_amount

    def gross_subtotal(self, tax_type=None):
        """Sum of gross amount of each invoice line."""
        result = sum(line.line_extension_amount for line in
                     self.lines_with_taxes(tax_type=tax_type))
        return round(result, 2)

    def subtotal(self, tax_type=None):
        """Gross amount before taxes.

            TotalGrossAmount - AllowanceTotalAmount + ChargeTotalAmount
        """
        # TODO global charges and discounts
        gross_subtotal = self.gross_subtotal(tax_type=tax_type)
        allowance_total_amount = 0
        charge_total_amount = 0
        return gross_subtotal - allowance_total_amount + charge_total_amount

    def total(self):
        return self.subtotal() + self.tax_amount()

    # Properties so we can return what was in the XML instead of computing it
    # in case we read the invoice.
    @property
    def line_extension_amount(self):
        return self.gross_subtotal()

    @property
    def tax_exclusive_amount(self):
        return self.subtotal()

    @property
    def tax_inclusive_amount(self):
        return self.total()

    @property
    def payable_amount(self):
        # TODO PrepaidAmount
        prepaid_amount = 0
        return self.total() - prepaid_amount
