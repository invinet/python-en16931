from datetime import datetime
import lxml.etree

from money.currency import Currency

from en16931.entity import Entity
from en16931.money import MyMoney
from en16931.utils import parse_date
from en16931.utils import parse_money
from en16931.xpaths import get_from_xpath
from en16931.xpaths import get_entity
from en16931.xpaths import get_invoice_lines
from en16931.xpaths import get_discount
from en16931.xpaths import get_charge

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
        self._charge_amount = None
        self._charge_percent = None
        self._discount_amount = None
        self._discount_percent = None
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
        # discount and charge
        discount = get_discount(root)
        if discount is not None:
            invoice.discount = discount
        charge = get_charge(root)
        if charge is not None:
            invoice.charge = charge
        return invoice

    @property
    def currency(self):
        return self._currency.name

    @currency.setter
    def currency(self, currency_str):
        try:
            self._currency = Currency[currency_str]
        except KeyError:
            raise KeyError('Currency {} not suported'.format(currency_str))

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

    @property
    def charge(self):
        if self._charge_amount is not None:
            return self._charge_amount
        else:
            return MyMoney('0', self._currency)

    @charge.setter
    def charge(self, value):
        self._charge_amount = parse_money(value, self._currency)
        self._charge_percent = round(self._charge_amount / self.gross_subtotal(), 2)

    @property
    def charge_percent(self):
        return self._charge_percent

    @property
    def charge_base_amount(self):
        if self._charge_amount is not None and self._charge_percent is not None:
            return self._charge_amount / self._charge_percent

    @property
    def discount(self):
        if self._discount_amount is not None:
            return self._discount_amount
        else:
            return MyMoney('0', self._currency)

    @discount.setter
    def discount(self, value):
        self._discount_amount = parse_money(value, self._currency)
        self._discount_percent = round(self._discount_amount / self.gross_subtotal(), 2)

    @property
    def discount_percent(self):
        return self._discount_percent

    @property
    def discount_base_amount(self):
        if self._discount_amount is not None and self._discount_percent is not None:
            return self._discount_amount / self._discount_percent

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
        result = (self.taxable_base(tax_type=tax) * tax.percent for tax in taxes)
        return sum(result, MyMoney('0', self._currency))

    def taxable_base(self, tax_type=None):
        return self.gross_subtotal(tax_type=tax_type) - self.discount + self.charge

    def gross_subtotal(self, tax_type=None):
        """Sum of gross amount of each invoice line."""
        amounts = (line.line_extension_amount for line in
                   self.lines_with_taxes(tax_type=tax_type))
        return sum(amounts, MyMoney('0', self._currency))

    def subtotal(self, tax_type=None):
        """Gross amount before taxes.

            TotalGrossAmount - AllowanceTotalAmount + ChargeTotalAmount
        """
        gross_subtotal = self.gross_subtotal(tax_type=tax_type)
        return gross_subtotal - self.discount + self.charge

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
        self._line_extension_amount = parse_money(value, self._currency)

    @property
    def tax_exclusive_amount(self):
        if self._tax_exclusive_amount is not None:
            return self._tax_exclusive_amount
        return self.subtotal()

    @tax_exclusive_amount.setter
    def tax_exclusive_amount(self, value):
        self._tax_exclusive_amount = parse_money(value, self._currency)

    @property
    def tax_inclusive_amount(self):
        if self._tax_inclusive_amount is not None:
            return self._tax_inclusive_amount
        return self.total()

    @tax_inclusive_amount.setter
    def tax_inclusive_amount(self, value):
        self._tax_inclusive_amount = parse_money(value, self._currency)

    @property
    def payable_amount(self):
        if self._payable_amount is not None:
            return self._payable_amount
        # TODO PrepaidAmount
        prepaid_amount = MyMoney('0', self._currency)
        return self.total() - prepaid_amount

    @payable_amount.setter
    def payable_amount(self, value):
        self._payable_amount = parse_money(value, self._currency)
