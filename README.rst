python-en16931
==============

.. image:: https://travis-ci.org/invinet/python-en16931.svg?branch=master
    :target: https://travis-ci.org/invinet/python-en16931

.. image:: https://codecov.io/gh/invinet/python-en16931/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/invinet/python-en16931

Python 3 package to read, write and manage the new `EN16931 Invoice format <http://docs.peppol.eu/poacc/billing/3.0/bis/>`_.

This `European Standard <https://standards.cen.eu/dyn/www/f?p=204:110:0::::FSP_PROJECT:60602&cs=1B61B766636F9FB34B7DBD72CE9026C72>`_ establishes a semantic data model of the core elements of an electronic invoice. The semantic model includes only the essential information elements that an electronic invoice needs to ensure legal (including fiscal) compliance and to enable interoperability for cross-border, cross sector and for domestic trade.

Features
--------

This library allows you to:

1. De-serialize an XML in EN16931 format to a python Invoice object.
2. Serialize a python Invoice object to a valid XML representation.
3. Validate an Invoice using `validex <https://open.validex.net>`_.
4. Import an Invoice to `B2BRouter <https://www.b2brouter.net/>`_.

Installation
------------

You can use pip to install this package:

.. code-block:: bash
    
    $ pip install en16931

Usage
-----

You can import an invoice from an XML file:

.. code-block:: python

    >>> from en16931 import Invoice
    >>> invoice = Invoice.from_xml('en16931/tests/files/invoice.xml')

And use the API to access its internal values and entities:

.. code-block:: python

    >>> invoice.issue_date
    datetime.datetime(2018, 6, 11, 0, 0)
    >>> invoice.seller_party
    <en16931.entity.Entity at 0x7f2b7c12b860>
    >>> invoice.buyer_party
    <en16931.entity.Entity at 0x7f2b7c0fd160>
    >>> invoice.unique_taxes
    { Tax S: 0.21  , Tax S: 0.1  }
    >>> invoice.lines
    [<en16931.invoice_line.InvoiceLine at 0x7f2b7c0fd400>,
     <en16931.invoice_line.InvoiceLine at 0x7f2b7c0fd518>,
     <en16931.invoice_line.InvoiceLine at 0x7f2b7c0fd748>]
    >>> invoice.tax_exclusive_amount
    87.00
    >>> invoice.tax_amount()
    16.62
    >>> invoice.tax_inclusive_amount
    103.62
    >>> invoice.payable_amount
    103.62

If you import an XML file, all relevant quantities are not computed; we
use the ones defined on the XML. You can check that the computed and
imported quantities match by calling the relevant methods: 

.. code-block:: python

    >>> assert invoice.tax_exclusive_amount == invoice.subtotal()
    True
    >>> assert invoice.tax_inclusive_amount == invoice.total()
    True
    >>> assert invoice.payable_amount == invoice.total()
    True

Or you can also build, step by step, an invoice:

.. code-block:: python

    >>> from en16931 import Invoice, Entity, InvoiceLine
    >>> invoice = Invoice(invoice_id="2018-01", currency="EUR")
    >>> seller = Entity(name="Acme Inc.", tax_scheme="VAT",
    ...                 tax_scheme_id="ES34626691F", country="ES",
    ...                 party_legal_entity_id="ES34626691F",
    ...                 registration_name="Acme INc.", mail="acme@acme.io",
    ...                 endpoint="ES76281415Y", endpoint_scheme="ES:VAT",
    ...                 address="easy street", postalzone="08080",
    ...                 city="Barcelona", province="Barcelona")
    >>> buyer = Entity(name="Corp Inc.", tax_scheme="VAT",
    ...                tax_scheme_id="ES76281415Y", country="ES",
    ...                party_legal_entity_id="ES76281415Y",
    ...                registration_name="Corp INc.", mail="corp@corp.io",
    ...                endpoint="ES76281415Y", endpoint_scheme="ES:VAT",
    ...                address="busy street", postalzone="08080",
    ...                city="Barcelona", province="Barcelona")
    >>> invoice.buyer_party = buyer
    >>> invoice.seller_party = seller
    >>> invoice.due_date = "2018-09-11"
    >>> invoice.issue_date = "2018-06-11"
    >>> # lines
    >>> il1 = InvoiceLine(quantity=11, unit_code="EA", price=2,
    ...                   item_name='test 1', currency="EUR",
    ...                   tax_percent=0.21, tax_category="S")
    >>> il2 = InvoiceLine(quantity=2, unit_code="EA", price=25,
    ...                   item_name='test 2', currency="EUR",
    ...                   tax_percent=0.21, tax_category="S")
    >>> il3 = InvoiceLine(quantity=5, unit_code="EA", price=3,
    ...                   item_name='test 3', currency="EUR",
    ...                   tax_percent=0.1, tax_category="S")
    >>> invoice.add_lines_from([il1, il2, il3])
 
And serialize it to XML:

.. code-block:: python

    >>> # As a string
    >>> xml = invoice.to_xml()
    >>> # Or save it directly to a file
    >>> invoice.save('example_invoice.xml')

Limitations
-----------

This is a proof of concept implementation and not all features defined
in the EN16931 standard are implemented. But it is easy, in some cases
trivial, to implement them. The main not implemented features are:

* CreditNotes are not supported.
* File attachments are not supported.
* Delivery information is not supported.
* Only global charges and discounts are supported. Line discounts and
  charges are not supported.
* Other potentially useful attributes (such as InvoicePeriod, BuyerReference,
  OrderReference, BillingReference, ContractDocumentReference, among others)
  are not implemented.

If you need a particular feature implemented, see the following section
for feature requests.

Bugs and Feature Requests
-------------------------

Please report any bugs that you find `here <https://github.com/invinet/python-en16931/issues>`_.
Or, even better, fork the repository on `GitHub <https://github.com/invinet/python-en16931>`_
and create a pull request (PR). We welcome all changes, big or small.

License
-------

Released under the Apache License Version 2.0 (see `LICENSE.txt`)::

    Copyright (C) 2018 Invinet Sistemes
