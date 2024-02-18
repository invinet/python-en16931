import pytest
from collections.abc import Hashable

from en16931.tax import Tax


class TestTaxes:

    def test_initialization(self):
        t = Tax(0.21, "S", "IVA")
        assert t

    def test_hashable(self):
        t = Tax(0.21, "S", "IVA")
        assert isinstance(t, Hashable)

    def test_percent_less_than_one(self):
        t = Tax(0.21, "S", "IVA")
        assert t.percent == 0.21

    def test_percent_more_than_one(self):
        t = Tax(21, "S", "IVA")
        assert t.percent == 0.21

    def test_percent_string(self):
        t = Tax("21", "S", "IVA")
        assert t.percent == 0.21

    def test_cmp_with_None(self):
        t = Tax("21", "S", "IVA")
        assert not (t == None)

    def test_value_error_bad_percent(self):
        with pytest.raises(ValueError):
            t = Tax("asdf", "S", "IVA")

    def test_value_error_bad_category(self):
        with pytest.raises(ValueError):
            t = Tax("21", "asd", "IVA")
