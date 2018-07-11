"""
Bank information Class
"""

class BankInfo:
    """BankInfo class.

    Stores relevant banking information of :class:`Entity`
    to specify the needed information when the payment means
    of the invoice involves a Bank.

    You can initialize a BankInfo instance with all needed
    attributes:
    
    >>> b = BankInfo(account="1234567321", bic="AAAABBCCDDD",
    ...              mandate_reference_identifier="123")

    Or build it, step by step:

    >>> b = BankInfo()
    >>> b.account = "1234567321"
    >>> b.bic = "AAAABBCCDDD"
    >>> b.mandate_reference_identifier = "123"

    For the bank information to be complete it has to contain the
    IBAN number, or the bank account and the BIC. The mandate
    reference identifier is used in the context of debit payments.

    >>> b.is_valid()
    True

    """

    def __init__(self, account=None, iban=None, bic=None,
                 mandate_reference_identifier=None):
        """Initialize the Bank Information for an Entity.

        Parameters
        ----------
        account: string (optional)
            The bank account number.

        bic: string (optional)
            The Bank Identification Code of the account.

        iban: string (optional)
            The International Bank Account Number (IBAN)

        mandate_reference_identifier: string (optional)
            The Mandate Reference Identifier

        Notes
        -----
        For the bank information to be complete it has to contain the
        IBAN number, or the bank account and the BIC. The mandate
        reference identifier is used in the context of debit payments.

        """
        self.account = account
        self.iban = iban
        self.bic = bic
        self.mandate_reference_identifier = mandate_reference_identifier

    @property
    def account(self):
        """Property: Bank account number

        Parameters
        ----------
        account: string
            The bank account number.

        Notes
        -----
        No validation of the bank account number is performed.

        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the bank account number
        """
        self._account = account

    @property
    def iban(self):
        """Property: The International Bank Account Number (IBAN)

        Parameters
        ----------
        iban: string
            The International Bank Account Number (IBAN)

        Notes
        -----
        No validation of the IBAN is performed.

        """
        return self._iban

    @iban.setter
    def iban(self, iban):
        """Sets the IBAN
        """
        self._iban = iban

    @property
    def bic(self):
        """Property: The Bank Identification Code

        Also known as SWIFT code.

        Parameters
        ----------
        bic: string
            The Bank Identification Code of the account.

        Raises
        ------
        ValueError
            If the BIC code is not valid.

        Notes
        -----
        A BIC code has either 8 or 11 characters without
        dashes and spaces.

        """
        return self._bic

    @bic.setter
    def bic(self, bic):
        """Sets the Bank Identification Code
        """
        if bic is None or len(bic) == 8 or len(bic) == 11:
            self._bic = bic
        else:
            raise ValueError("A BIC code has either 8 or 11 charcters")

    @property
    def mandate_reference_identifier(self):
        """Property: The Mandate Reference Identifier

        The Mandate Reference Identifier is necessary for debit
        payments.

        Parameters
        ----------
        mandate_reference_identifier: string
            The Mandate Reference Identifier

        """
        return self._mandate_reference_identifier

    @mandate_reference_identifier.setter
    def mandate_reference_identifier(self, mandate_reference_identifier):
        """Sets the Mandate Reference Identifier
        """
        self._mandate_reference_identifier = mandate_reference_identifier

    def is_valid(self):
        """Returns True if the information is complete.

        A valid bank information for an :class:`Entity` must have a bank
        account and a BIC or an IBAN.
        """
        has_account = self._account is not None and self._bic is not None
        has_iban = self._iban is not None
        return has_account or has_iban

    def has_mandate_reference(self):
        """Returns True if it has a mandate reference identifier.

        This is necessary for debit payments.
        """
        return self._mandate_reference_identifier is not None
