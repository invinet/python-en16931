import os
import pytest
from datetime import datetime
from decimal import Decimal

from en16931.entity import Entity
from en16931.invoice import Invoice
from en16931.invoice_line import InvoiceLine
from en16931.tax import Tax


class TestInvoiceAttributes:

    def test_default_id_number(self):
        i = Invoice()
        assert i.invoice_id == '1'

    def test_id_number(self):
        i = Invoice(invoice_id="1-2018")
        assert i.invoice_id == "1-2018"

    def test_set_issue_date(self):
        dts = {
            "2018-09-11": "%Y-%m-%d",
            "20180911": "%Y%m%d",
            "21-06-2018": "%d-%m-%Y",
            "2018/12/12": "%Y/%m/%d",
            "12/12/2018": "%d/%m/%Y",
        }
        i = Invoice()
        for date, fmt in dts.items():
            i.issue_date = date
            assert i.issue_date.strftime(fmt) == date

    def test_set_dates_none(self):
        i = Invoice()
        i.issue_date = None
        assert i.issue_date is None
        i.due_date = None
        assert i.due_date is None

    def test_set_dates_datetime(self):
        i = Invoice()
        i.issue_date = datetime(2018, 7, 10)
        assert i.issue_date == datetime(2018, 7, 10)
        i.due_date = datetime(2018, 9, 10)
        assert i.due_date == datetime(2018, 9, 10)

    def test_wrong_issue_date(self):
        with pytest.raises(ValueError):
            i = Invoice()
            i.issue_date = "asdef"
        with pytest.raises(ValueError):
            i = Invoice()
            i.issue_date = 123

    def test_set_due_date(self):
        dts = {
            "2018-09-11": "%Y-%m-%d",
            "20180911": "%Y%m%d",
            "21-06-2018": "%d-%m-%Y",
            "2018/12/12": "%Y/%m/%d",
            "12/12/2018": "%d/%m/%Y",
        }
        i = Invoice()
        for date, fmt in dts.items():
            i.due_date = date
            assert i.due_date.strftime(fmt) == date

    def test_wrong_due_date(self):
        with pytest.raises(ValueError):
            i = Invoice()
            i.due_date = "asdef"
        with pytest.raises(ValueError):
            i = Invoice()
            i.due_date = 123

    def test_invalid_currency(self):
        with pytest.raises(KeyError):
            i = Invoice()
            i.currency = "asdef"

    def test_wrong_seller_entity(self):
        with pytest.raises(TypeError):
            i = Invoice()
            i.seller_party = 123
        with pytest.raises(ValueError):
            i = Invoice()
            i.seller_party = Entity()

    def test_wrong_buyer_entity(self):
        with pytest.raises(TypeError):
            i = Invoice()
            i.buyer_party = 123
        with pytest.raises(ValueError):
            i = Invoice()
            i.buyer_party = Entity()

    def test_invalid_payment_code(self):
        with pytest.raises(ValueError):
            i = Invoice()
            i.payment_means_code = "asdef"

    def test_payment_code(self):
            i = Invoice()
            i.payment_means_code = "10"
            assert i.payment_means_code == "10"


class TestInvoiceOperations:

    def test_unique_taxes(self, invoice1, tax1, tax2):
        assert len(invoice1.unique_taxes) == 2
        assert invoice1.unique_taxes == {tax1, tax2}

    def test_lines_with_taxes(self, invoice1, tax1, tax2):
        assert len(list(invoice1.lines_with_taxes(tax_type=tax1))) == 2
        assert len(list(invoice1.lines_with_taxes(tax_type=tax2))) == 1

    def test_tax_amount(self, invoice1, tax1, tax2):
        assert str(invoice1.tax_amount()) == '16.62'
        assert str(invoice1.tax_amount(tax_type=tax1)) == '15.12'
        assert str(invoice1.tax_amount(tax_type=tax2)) == '1.50'

    def test_taxable_base(self, invoice1, tax1, tax2):
        assert str(invoice1.taxable_base()) == '87.00'
        assert str(invoice1.taxable_base(tax_type=tax1)) == '72.00'
        assert str(invoice1.taxable_base(tax_type=tax2)) == '15.00'

    def test_gross_subtotal(self, invoice1):
        assert str(invoice1.gross_subtotal()) == '87.00'

    def test_subtotal(self, invoice1):
        assert str(invoice1.gross_subtotal()) == '87.00'

    def test_total(self, invoice1):
        assert str(invoice1.total()) == '103.62'

    def test_line_extension_amount(self, invoice1):
        assert str(invoice1.line_extension_amount) == '87.00'

    def test_tax_exclusive_amount(self, invoice1):
        assert str(invoice1.tax_exclusive_amount) == '87.00'

    def test_tax_inclusive_amount(self, invoice1):
        assert str(invoice1.tax_inclusive_amount) == '103.62'

    def test_payable_amount(self, invoice1):
        assert str(invoice1.payable_amount) == '103.62'

    def test_charge_amount(self, invoice1):
        assert str(invoice1.charge_amount) == '0.00'
        invoice1.charge_amount = 10
        assert str(invoice1.charge_amount) == '10.00'
        assert str(invoice1.subtotal()) == '97.00'

    def test_discount_amount(self, invoice1):
        assert str(invoice1.discount_amount) == '0.00'
        invoice1.discount_amount = 10
        assert str(invoice1.discount_amount) == '10.00'
        assert str(invoice1.subtotal()) == '77.00'

    def test_charge_percent(self, invoice1):
        invoice1.charge_percent = 10
        assert str(invoice1.charge_percent) == '0.1'
        assert str(invoice1.charge_amount) == '8.70'
        assert str(invoice1.subtotal()) == '95.70'

    def test_discount_percent(self, invoice1):
        invoice1.discount_percent = 10
        assert str(invoice1.discount_percent) == '0.1'
        assert str(invoice1.discount_amount) == '8.70'
        assert str(invoice1.subtotal()) == '78.30'



class TestInvoiceXMLGeneration:

    def test_generates_xml_invoice1(self, invoice1):
        out = invoice1.to_xml()
        assert len(out) > 0

    def test_generates_xml_invoice2(self, invoice2):
        out = invoice2.to_xml()
        assert len(out) > 0

    def test_generates_xml_invoice3(self, invoice3):
        out = invoice3.to_xml()
        assert len(out) > 0

    def test_writes_xml_file_invoice1(self, invoice1):
        path = '/tmp/invoice1.xml'
        invoice1.save(path)
        assert os.path.exists(path)

    def test_writes_xml_file_invoice2_with_discount_and_charge(self, invoice2):
        path = '/tmp/invoice2.xml'
        invoice2.save(path)
        assert os.path.exists(path)

    def test_writes_xml_file_invoice3_with_payment_means(self, invoice3):
        path = '/tmp/invoice3.xml'
        invoice3.save(path)
        assert os.path.exists(path)
