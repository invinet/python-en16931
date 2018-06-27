from en16931.utils import parse_float


UNIT_CODES = {
    'EA': 'units',
    'HUR':'hours',
    'KGM':'kilograms',
    'LTR':'litters',
    'DAY':'days',    
    'CS': 'boxes',
}

CURRENCIES = {"EUR", "USD"}


class InvoiceLine:

    def __init__(self, quantity=None, unit_code="EA", price=None, item_name=None, currency="EUR"):
        self.item_name = item_name
        self.quantity = quantity
        self.unit_code = unit_code
        self.price = price
        self.currency = currency


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
        try:
            self._price = parse_float(price)
        except ValueError:
            raise ValueError("Unrecognized price {}".format(price))


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
        return self._quantity is not None and self._price is not None


    @property
    def line_extension_amount(self):
        # TODO deal better with rounding issues
        if self.is_valid:
            return round(self._price * self._quantity, 2)
        else:
            raise ValueError("Price or quantity not set for this line")
