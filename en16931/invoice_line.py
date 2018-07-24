"""
Class for representing an invoice line.
"""
from money.money import Money
from money.currency import Currency

from en16931.tax import Tax
from en16931.utils import parse_float
from en16931.utils import parse_money


UNIT_CODES = {
    'EA': 'units',
    'HUR': 'hours',
    'KGM': 'kilograms',
    'LTR': 'litters',
    'DAY': 'days',
    'CS': 'boxes',
}


class InvoiceLine:
    """EN16931 InvoiceLine class.

    Each :class:`Invoice` has to have at least one invoice
    line in which the quantity and the price of the items is
    reflected.

    You can initialize an InvoiceLine instance with all its
    attributes:

    >>> il = InvoiceLine(quantity=11, unit_code="EA", price=2,
    ...                  item_name='test', currency="EUR",
    ...                  tax_percent=0.21, tax_category="S")

    Or cou can do it step by step:

    >>> il = InvoiceLine()
    >>> il.quantity = 11
    >>> il.price = 2
    >>> il.item_name = 'test'
    >>> il.tax_percent = 0.21
    >>> il.tax_category = "S"

    An InvoiceLine is only valid if it has quantity, price and
    tax defined:

    >>> il.is_valid()
    True
    >>> new_line = InvoiceLine()
    >>> new_line.is_valid()
    False

    """

    def __init__(self, quantity=None, unit_code="EA", price=None,
                 item_name=None, currency="EUR", tax_percent=None,
                 line_extension_amount=None, tax_category=None,
                 tax_name=None):
        """Initialize an Invoice Line.

        Parameters
        ----------
        quantity: float or integer.
            The number of items of the line.

        unit_code: string (optional).
            A unit code defining the nature of the quantities of the
            items of the line. It must be one of: 'EA': 'units',
            'HUR': 'hours', 'KGM': 'kilograms', 'LTR': 'litters',
            'DAY': 'days', 'CS': 'boxes'.

        price: string, integer, float
            The input must be a valid input for the Decimal class
            the Python Standard Library.

        item_name: string (optional).
            Arbitrary name to define the item of the line.

        currency: string.
            String representation of the ISO 4217 currency code.

        tax_percent: float.
            The percentage of the Tax applied to the line.
            Can be 0.

        tax_category: string.
            A string representing the category of the Tax.
            It must be one of 'AE', 'L', 'M', 'E', 'S', 'Z',
            'G', 'O', or 'K'.

        tax_name: string.
            Arbitrary name to identify the Tax.

        line_extension_amount: string, integer, float
            The input must be a valid input for the Decimal class
            the Python Standard Library. Computed unless the invoice
            is imported from an XML file.


        Notes
        -----
        An InvoiceLine is considered valid if and only if it has quantity,
        price and tax.

        """
        self.currency = currency
        self.item_name = item_name
        self.quantity = quantity
        self.unit_code = unit_code
        self.price = price
        self.line_extension_amount = line_extension_amount
        self.tax_percent = tax_percent
        self.tax_category = tax_category
        self.tax_name = tax_name

    @property
    def currency(self):
        """Property: String representation of the ISO 4217 currency code.

        Parameters
        ----------
        currency_str: string
            String representation of the ISO 4217 currency code.

        Raises
        ------
        KeyError: If the currency code is not a valid ISO 4217 code.

        """
        return self._currency.name

    @currency.setter
    def currency(self, currency_str):
        """Sets the currency of the Invoice.
        """
        try:
            self._currency = Currency[currency_str]
        except KeyError:
            raise KeyError('Currency {} not suported'.format(currency_str))

    @property
    def tax(self):
        """Returns a Tax object representing the taxes applied to the line.
        """
        if self.tax_percent and self.tax_category:
            return Tax(self.tax_percent, self.tax_category, self.tax_name or "")
        else:
            return None

    @property
    def item_name(self):
        """The arbitrary name of the item of the line.

        Parameters
        ----------
        item_name: string (optional).
            Arbitrary name to define the item of the line.

        """
        return self._item_name

    @item_name.setter
    def item_name(self, name):
        """Sets the arbitrary name of the item of the line.
        """
        self._item_name = name

    @property
    def quantity(self):
        """Property: Quantity of items of the line.

        Parameters
        ---------
        quantity: float or integer.
            The number of items of the line.

        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of items of the line.
        """
        try:
            self._quantity = parse_float(quantity)
        except ValueError:
            raise ValueError("Unrecognized quantity {}".format(quantity))

    @property
    def price(self):
        """Property: The price of one item.

        Parameters
        ---------
        price: string, integer, float
            The input must be a valid input for the Decimal class
            the Python Standard Library.

        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of one item.
        """
        if price is None:
            return
        try:
            self._price = parse_money(price, self._currency)
            self._line_extension_amount = self._price * self._quantity
        except ValueError:
            raise ValueError("Unrecognized price {}".format(price))

    @property
    def line_extension_amount(self):
        """Property: The LineExtensionAmount

        Parameters
        ---------
        line_extension_amount: string, integer, float
            The input must be a valid input for the Decimal class
            the Python Standard Library. Computed unless the invoice
            is imported from an XML file.


        """
        if self._line_extension_amount is not None:
            return self._line_extension_amount
        else:
            return self._price * self._quantity

    @line_extension_amount.setter
    def line_extension_amount(self, price):
        """Sets the LineExtensionAmount.
        """
        if price is None:
            return
        try:
            self._line_extension_amount = parse_money(price, self._currency)
        except ValueError:
            raise ValueError("Unrecognized line_extension_amount {}".format(price))

    @property
    def unit_code(self):
        """property: The unit code defining the nature of the quantities.

        Parameters
        ----------
        unit_code: string.
            A unit code defining the nature of the quantities of the
            items of the line. It must be one of: 'EA': 'units',
            'HUR': 'hours', 'KGM': 'kilograms', 'LTR': 'litters',
            'DAY': 'days', 'CS': 'boxes'.

        """
        return self._unit_code

    @unit_code.setter
    def unit_code(self, code):
        """Sets the unit code defining the nature of the quantities.
        """
        if code not in UNIT_CODES:
            raise ValueError("Unsupported unit code {}".format(code))
        self._unit_code = code

    def is_valid(self):
        """Returns True if the line is valid.
        """
        has_quantity = self._quantity is not None
        has_price = self._price is not None
        has_tax = self.tax is not None
        return has_quantity and has_price and has_tax

    def has_tax(self, tax):
        """Returns True if the line has this tax.

        Parameters
        ----------
        tax: Tax Object.
            
        """
        if tax is None:
            return True
        return self.tax == tax

    def __repr__(self):
        if not self.is_valid():
            return "{}: empty".format(self.__class__)
        return "{}: {} {} x {} {}".format(self.__class__, self.quantity,
                                          self.item_name, self.price,
                                          self.currency)
