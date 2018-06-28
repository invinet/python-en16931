import pytest
from collections import Hashable

from en16931.tax import Tax


class TestTaxes:

    def test_initialization(self):
        t = Tax(0.21, "AA", "IVA")
        assert t

    def test_hashable(self):
        t = Tax(0.21, "AA", "IVA")
        assert isinstance(t, Hashable)

    def test_percent_less_than_one(self):
        t = Tax(0.21, "AA", "IVA")
        assert t.percent == 0.21

    def test_percent_more_than_one(self):
        t = Tax(21, "AA", "IVA")
        assert t.percent == 0.21

    def test_percent_string(self):
        t = Tax("21", "AA", "IVA")
        assert t.percent == 0.21

    def test_value_error_bad_percent(self):
        with pytest.raises(ValueError):
            t = Tax("asdf", "AA", "IVA")
