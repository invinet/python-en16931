from en16931.utils import parse_float


class Tax:

    def __init__(self, percent, category, name, comment=""):
        self.category = category
        self.name = name
        self.comment = comment
        pct = parse_float(percent)
        if pct > 1 or pct < -1:
            self.percent = pct / 100
        else:
            self.percent = pct

    @property
    def code(self):
        return "{}_{}".format(self.percent, self.category)

    def __eq__(self, other):
        if other is None:
            return False
        return (self.percent == other.percent and
                self.category == self.category and
                self.name == self.name)

    def __hash__(self):
        return hash(self.code)

    def __repr__(self):
        return "Tax {}: {} {} {}".format(self.category, self.percent,
                                         self.name, self.comment)
