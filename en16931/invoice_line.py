from en16931.tax import Tax
from en16931.utils import parse_float


UNIT_CODES = {
    'EA': 'units',
    'HUR': 'hours',
    'KGM': 'kilograms',
    'LTR': 'litters',
    'DAY': 'days',
    'CS': 'boxes',
}

CURRENCIES = {"EUR", "USD"}


class InvoiceLine:

    def __init__(self, quantity=None, unit_code="EA", price=None,
                 item_name=None, currency="EUR", tax_percent=None,
                 line_extension_amount=None, tax_category=None,
                 tax_name=None):
        self.item_name = item_name
        self.quantity = quantity
        self.unit_code = unit_code
        self.price = price
        self.line_extension_amount = line_extension_amount
        self.currency = currency
        self.tax_percent = tax_percent
        self.tax_category = tax_category
        self.tax_name = tax_name

    @property
    def tax(self):
        if self.tax_percent and self.tax_category:
            return Tax(self.tax_percent, self.tax_category, self.tax_name or "")
        else:
            return None

    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, name):
        self._item_name = name

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        try:
            self._quantity = parse_float(quantity)
        except ValueError:
            raise ValueError("Unrecognized quantity {}".format(quantity))

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if price is None:
            return
        try:
            self._price = parse_float(price)
            self._line_extension_amount = round(self._price * self._quantity, 2)
        except ValueError:
            raise ValueError("Unrecognized price {}".format(price))

    @property
    def line_extension_amount(self):
        return self._line_extension_amount

    @line_extension_amount.setter
    def line_extension_amount(self, price):
        if price is None:
            return
        try:
            self._line_extension_amount = parse_float(price)
            self._price = round(self._line_extension_amount / self.quantity, 2)
        except ValueError:
            raise ValueError("Unrecognized line_extension_amount {}".format(price))

    @property
    def unit_code(self):
        return self._unit_code

    @unit_code.setter
    def unit_code(self, code):
        if code not in UNIT_CODES:
            raise ValueError("Unsupported unit code {}".format(code))
        self._unit_code = code

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, currency):
        if currency not in CURRENCIES:
            raise ValueError("Unsupported currency {}".format(currency))
        self._currency = currency

    def is_valid(self):
        has_quantity = self._quantity is not None
        has_price = self._price is not None
        has_tax = self.tax is not None
        return has_quantity and has_price and has_tax

    def has_tax(self, tax):
        if tax is None:
            return True
        return self.tax == tax
