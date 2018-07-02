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
        assert invoice.line_extension_amount == 87.00
        assert invoice.tax_exclusive_amount == 87.00
        assert invoice.tax_inclusive_amount == 103.62
        assert invoice.payable_amount == 103.62
        # Check imported lines by computing the values of
        # totals from lines and comparing them to those from
        # the XML.
        assert invoice.line_extension_amount == invoice.subtotal()
        assert invoice.tax_exclusive_amount == invoice.subtotal()
        assert invoice.tax_inclusive_amount == invoice.total()
        assert invoice.payable_amount == invoice.total()
