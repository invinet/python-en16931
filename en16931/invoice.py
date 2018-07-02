from datetime import datetime
import lxml.etree

from en16931.entity import Entity
from en16931.utils import parse_date
from en16931.utils import parse_float
from en16931.xpaths import get_from_xpath
from en16931.xpaths import get_entity
from en16931.xpaths import get_invoice_lines

from jinja2 import Environment, PackageLoader

templates = Environment(loader=PackageLoader('en16931', 'templates'))

class Invoice:

    def __init__(self, invoice_id=None, currency="EUR", from_xml=False):
        self.invoice_id = invoice_id or 1
        self.currency = currency
        self.ubl_version_id = "2.1"
        self.customization_id = "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0"
        self.profile_id = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
        self.invoice_type_code = 380
        self._issue_date = None
        self._due_date = None
        self._seller_party = None
        self._buyer_party = None
        self._templates = templates.get_template('invoice.xml')
        self._imported_from_xml = from_xml
        self._line_extension_amount = None
        self._tax_exclusive_amount = None
        self._tax_inclusive_amount = None
        self._payable_amount = None
        self.lines = []

    @classmethod
    def from_xml(cls, xml_path):
        with open(xml_path, "rb") as f:
            xml = f.read()
        root = lxml.etree.fromstring(xml)
        invoice_id = get_from_xpath(root, "invoice_id")
        currency = get_from_xpath(root, "currency")
        invoice = cls(invoice_id=invoice_id, currency=currency, from_xml=True)
        invoice.issue_date = get_from_xpath(root, "invoice_issue_date")
        invoice.due_date = get_from_xpath(root, "invoice_due_date")
        # seller and buyer
        invoice.seller_party = get_entity(root, kind='seller')
        invoice.buyer_party = get_entity(root, kind='buyer')
        # totals
        invoice.line_extension_amount = get_from_xpath(root, "invoice_line_extension_amount")
        invoice.tax_exclusive_amount = get_from_xpath(root, "tax_exclusive_amount")
        invoice.tax_inclusive_amount = get_from_xpath(root, "tax_inclusive_amount")
        invoice.payable_amount = get_from_xpath(root, "payable_amount")
        # lines
        invoice.add_lines_from(get_invoice_lines(root))
        return invoice

    def to_xml(self):
        return self._templates.render(invoice=self)

    def save(self, path=None):
        if path is None:
            path = 'invoice_{}.xml'.format(self.invoice_id)
        with open(path, 'w') as f:
            f.write(self.to_xml())

    @property
    def issue_date(self):
        return self._issue_date

    @issue_date.setter
    def issue_date(self, date):
        if not date:
            return
        elif isinstance(date, datetime):
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
        if not date:
            return
        elif isinstance(date, datetime):
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
        if self._line_extension_amount is not None:
            return self._line_extension_amount
        return self.gross_subtotal()

    @line_extension_amount.setter
    def line_extension_amount(self, value):
        self._line_extension_amount = parse_float(value)

    @property
    def tax_exclusive_amount(self):
        if self._tax_exclusive_amount is not None:
            return self._tax_exclusive_amount
        return self.subtotal()

    @tax_exclusive_amount.setter
    def tax_exclusive_amount(self, value):
        self._tax_exclusive_amount = parse_float(value)

    @property
    def tax_inclusive_amount(self):
        if self._tax_inclusive_amount is not None:
            return self._tax_inclusive_amount
        return self.total()

    @tax_inclusive_amount.setter
    def tax_inclusive_amount(self, value):
        self._tax_inclusive_amount = parse_float(value)

    @property
    def payable_amount(self):
        if self._payable_amount is not None:
            return self._payable_amount
        # TODO PrepaidAmount
        prepaid_amount = 0
        return self.total() - prepaid_amount

    @payable_amount.setter
    def payable_amount(self, value):
        self._payable_amount = parse_float(value)
