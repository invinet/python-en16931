from decimal import Decimal

from money.money import Money
from money.currency import Currency

class MyMoney(Money):

    def __init__(self, amount, currency=Currency.EUR):
        # Allow initialization with an arbitrary number of
        # decimal places but round it to the correct number
        # of decimal places at initialization.
        self._amount = self._round(Decimal(amount), currency)
        self._currency = currency

    def __repr__(self):
        # Omit currency in the repr
        return "{}".format(self._amount)
