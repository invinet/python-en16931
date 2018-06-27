import pytest

from invoice import Invoice
from entity import Entity
from invoice_line import InvoiceLine


class TestInvoice:

    def test_default_id_number(self):
        i = Invoice()
        assert i.invoice_id == 1

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

    def test_wrong_issue_date(self):
        with pytest.raises(ValueError):
            i = Invoice()
            i.issue_date = "asdef"

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
