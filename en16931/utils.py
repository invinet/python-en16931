"""
Miscelanious util functions
"""
from datetime import datetime
from decimal import InvalidOperation

from en16931.money import MyMoney

def parse_money(amount, currency):
    if amount is None:
        return None
    elif isinstance(amount, MyMoney):
        return amount
    try:
        return MyMoney(amount, currency)
    except InvalidOperation:
        raise ValueError('Could not convert {} to money'.format(amount))


def parse_float(flt):
    if flt is None:
        return None
    try:
        return float(flt)
    except ValueError:
        raise ValueError('Could not convert {} to float'.format(flt))


def parse_date(date):
    formats = [
        "%Y-%m-%d",
        "%Y%m%d",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d/%m/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            continue
    else:
        raise ValueError("See documentation for string date formats supported")
