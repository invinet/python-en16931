import pytest

from en16931.invoice_line import InvoiceLine


class TestInvoiceLine:

    def test_initialization(self):
        il = InvoiceLine(quantity=11, unit_code="EA", price=2,
                         item_name='test', currency="EUR",
                         tax_percent=0.21, tax_category="S")
        assert il.is_valid()
        assert il.currency == "EUR"

    def test_invalid_currency(self):
        il = InvoiceLine()
        with pytest.raises(KeyError):
            il.currency = "blah"

    def test_no_taxes(self):
        il = InvoiceLine()
        assert il.tax is None

    def test_creation(self):
        il = InvoiceLine()
        il.quantity = 11
        il.price = 2
        il.item_name = 'test'
        il.tax_percent = 0.21
        il.tax_category = "S"
        assert il.is_valid()

    def test_line_extension_amount(self):
        il = InvoiceLine(quantity=11, unit_code="EA", price=2,
                         item_name='test', currency="EUR",
                         tax_percent=0.21, tax_category="S")
        assert str(il.line_extension_amount) == '22.00'

    def test_invalid_unit_code(self):
        il = InvoiceLine()
        with pytest.raises(ValueError):
            il.unit_code = "ASF"

    def test_invalid_price(self):
        il = InvoiceLine()
        with pytest.raises(ValueError):
            il.price = "dasdas"

    def test_invalid_line_extension_amount(self):
        il = InvoiceLine()
        with pytest.raises(ValueError):
            il.line_extension_amount = "expensive"

    def test_invalid_quantity(self):
        il = InvoiceLine()
        with pytest.raises(ValueError):
            il.quantity = "dasdas"
