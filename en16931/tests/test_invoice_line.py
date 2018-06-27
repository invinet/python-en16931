import pytest

from invoice_line import InvoiceLine


class TestInvoiceLine:

    def test_initialization(self):
        il = InvoiceLine(quantity=11, unit_code="EA", price=2,
                         item_name='test', currency="EUR")
        assert il.is_valid()

    def test_creation(self):
        il = InvoiceLine()
        il.quantity = 11
        il.price = 2
        il.item_name = 'test'
        assert il.is_valid()

    def test_line_extension_amount(self):
        il = InvoiceLine(quantity=11, unit_code="EA", price=2,
                         item_name='test', currency="EUR")
        assert il.line_extension_amount == 22.0

    def test_invalid_unit_code(self):
        il = InvoiceLine()
        with pytest.raises(ValueError):
            il.unit_code = "ASF"

    def test_invalid_price(self):
        il = InvoiceLine()
        with pytest.raises(ValueError):
            il.price = "dasdas"

    def test_invalid_quantity(self):
        il = InvoiceLine()
        with pytest.raises(ValueError):
            il.quantity = "dasdas"
