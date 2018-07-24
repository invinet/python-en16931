import pytest

from en16931.invoice import Invoice


class TestImportInvoices:
    
    def test_imports_invoice1_xml(self, xml_path):
        invoice = Invoice.from_xml(xml_path)
        assert invoice.invoice_id == '1'
        assert invoice.issue_date.strftime("%Y-%m-%d") == "2018-06-11"
        assert invoice.due_date.strftime("%Y-%m-%d") == "2018-09-11"
        # Seller and buyer
        assert invoice.seller_party.is_valid()
        assert invoice.buyer_party.is_valid()
        # totals
        assert str(invoice.line_extension_amount) == '87.00'
        assert str(invoice.tax_exclusive_amount) == '87.00'
        assert str(invoice.tax_inclusive_amount) == '103.62'
        assert str(invoice.payable_amount) == '103.62'
        # Check imported lines by computing the values of
        # totals from lines and comparing them to those from
        # the XML.
        assert invoice.line_extension_amount == invoice.subtotal()
        assert invoice.tax_exclusive_amount == invoice.subtotal()
        assert invoice.tax_inclusive_amount == invoice.total()
        assert invoice.payable_amount == invoice.total()
        # Check that we stored the original xml
        with open(xml_path, 'rb') as fh:
            assert invoice.to_xml().encode('utf8') == fh.read()

    def test_imports_invoice2_xml(self, xml_path_invoice2):
        invoice = Invoice.from_xml(xml_path_invoice2)
        assert invoice.invoice_id == '1'
        assert invoice.issue_date.strftime("%Y-%m-%d") == "2018-06-11"
        assert invoice.due_date.strftime("%Y-%m-%d") == "2018-09-11"
        # Seller and buyer
        assert invoice.seller_party.is_valid()
        assert invoice.buyer_party.is_valid()
        # totals
        assert str(invoice.line_extension_amount) == '60.00'
        assert str(invoice.tax_exclusive_amount) == '50.00'
        assert str(invoice.tax_inclusive_amount) == '60.50'
        assert str(invoice.payable_amount) == '60.50'
        # discount and charge
        assert str(invoice.charge_amount) == '10.00'
        assert str(invoice.discount_amount) == '20.00'
        # Check imported lines by computing the values of
        # totals from lines and charges and discounts and
        # comparing them to those from the XML.
        assert invoice.tax_exclusive_amount == invoice.subtotal()
        assert invoice.tax_inclusive_amount == invoice.total()
        assert invoice.payable_amount == invoice.total()
        # Check that we stored the original xml
        with open(xml_path_invoice2, 'rb') as fh:
            assert invoice.to_xml().encode('utf8') == fh.read()
