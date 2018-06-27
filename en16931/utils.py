from datetime import datetime


def parse_float(flt):
    # TODO more sophistication (support , and . as decimal point)
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



