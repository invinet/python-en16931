import pytest

from en16931 import BankInfo


class TestBankInfo:

    def test_initialization_account_bic(self):
        b = BankInfo(account="1234567", bic="AAAABBCCDDD")
        assert b.is_valid()
        assert b.account == "1234567"
        assert b.bic == "AAAABBCCDDD"
    
    def test_initialization_iban(self):
        b = BankInfo(iban="ES661234567321")
        assert b.is_valid()
        assert b.iban == "ES661234567321"

    def test_iban_setter(self):
        b = BankInfo()
        assert not b.is_valid()
        b.iban = "ES661234567321"
        assert b.is_valid()
        assert b.iban == "ES661234567321"

    def test_account_bic_setter(self):
        b = BankInfo()
        assert not b.is_valid()
        b.account = "1234567321"
        b.bic = "AAAABBCCDDD"
        assert b.is_valid()
        assert b.account == "1234567321"
        assert b.bic == "AAAABBCCDDD"

    def test_invalid_bic(self):
        b = BankInfo()
        with pytest.raises(ValueError):
            b.bic = "foo"

    def test_mandate(self):
        b = BankInfo(account="1234567", bic="AAAABBCCDDD",
                     mandate_reference_identifier="123")
        assert b.is_valid()
        assert b.has_mandate_reference()
        assert b.mandate_reference_identifier == "123"
