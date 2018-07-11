"""
Class for representing a Tax category.
"""
from en16931.utils import parse_float


CATEGORIES = {'AE', 'L', 'M', 'E', 'S', 'Z', 'G', 'O', 'K'}


class Tax:
    """Tax class.

    It representas a tax to apply globally or to a concrete
    invoice line.

    Only categories of taxes enabled by the EN16931 standard are
    supported. See the documentation of :meth:`category` property
    for more details.

    You can create Tax objects directly:

    >>> t = Tax(0.21, "S", "IVA")

    Or specify the relevant attributes when building
    :class:`InvoiceLines` or :class:`Invoice`

    """

    def __init__(self, percent, category, name, comment=""):
        """Initialize a Tax object.

        Parameters
        ----------
        category: string.
            A string representing the category of the Tax.
            It must be one of 'AE', 'L', 'M', 'E', 'S', 'Z',
            'G', 'O', or 'K'.

        percent: float.
            The percentage of the Tax. Can be 0.

        name: string.
            Arbitrary name to identify the Tax.

        comment: string.
            A comment on the tax.

        Notes
        -----
        A tax is compared to other Tax objects by equality of their
        percentage, category, and name.

        """
        self.category = category
        self.name = name
        self.comment = comment
        pct = parse_float(percent)
        if pct > 1 or pct < -1:
            self.percent = pct / 100
        else:
            self.percent = pct

    @property
    def category(self):
        """Property: The category of the Tax.

        Parameters
        ----------
        category: string.
            A string representing the category of the Tax.
            It must be one of 'AE', 'L', 'M', 'E', 'S', 'Z',
            'G', 'O', or 'K'.

        Raises
        ------
        ValueError: if the category is not valid.

        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of the Tax.
        """
        if category not in CATEGORIES:
            msg = "Category {} not valid. Use one of {}"
            raise ValueError(msg.format(category, CATEGORIES))
        self._category = category

    @property
    def code(self):
        """An identification code of the tax.
        """
        return "{}_{}".format(self.percent, self.category)

    def __eq__(self, other):
        """
        A tax is compared to other Tax objects by equality of their
        percentage, category, and name.
        """
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
