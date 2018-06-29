from datetime import datetime


xpaths = None
namespaces = None

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


def get_from_xpath(root, tag, xpaths=None, namespaces=None):
    if xpaths is None:
        xpaths = get_xpaths()
    if namespaces is None:
        namespaces = get_namespaces()
    xpath = xpaths.get(tag)
    if xpath is None:
        raise KeyError("Unknown key {} for xpath".format(tag))
    result = root.xpath(xpath, namespaces=namespaces)
    if not result:
        return None
    return ", ".join(entry.text for entry in result)


def get_namespaces():
    global namespaces
    if namespaces is None:
        #print("loading namespace")
        namespaces = en16931_namespaces()
    return namespaces


def en16931_namespaces():
    namespaces = {
        "xmlns":"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
        "cac":"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        "cbc":"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    }
    return namespaces


def get_xpaths():
    global xpaths
    if xpaths is None:
        #print("loading xpaths")
        xpaths = en16931_xpaths()
    return xpaths


def en16931_xpaths():
    xpaths = {}
    xpaths["invoice_id"] = "/xmlns:Invoice/cbc:ID"
    xpaths["invoice_date"] = "/xmlns:Invoice/cbc:IssueDate"
    xpaths["invoice_issue_date"] = "/xmlns:Invoice/cbc:IssueDate"
    xpaths["extra_info"] = "/xmlns:Invoice/cbc:Note"
    xpaths["tax_point_date"] = "/xmlns:Invoice/cbc:TaxPointDate"
    xpaths["invoice_total"] = "/xmlns:Invoice/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount"
    xpaths["invoice_import"] = "/xmlns:Invoice/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount"
    xpaths["payment_method"] = "/xmlns:Invoice/cac:PaymentMeans/cbc:PaymentMeansCode"
    xpaths["invoice_due_date"] = "/xmlns:Invoice/cac:PaymentMeans/cbc:PaymentDueDate"
    xpaths["seller_taxcode"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID"
    xpaths["seller_party_legal_entity_id"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID"
    xpaths["seller_endpoint"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cbc:EndpointID"
    xpaths["seller_endpoint_scheme"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cbc:EndpointID/@schemeID"
    xpaths["seller_name"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name"
    xpaths["seller_address"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:StreetName"
    xpaths["seller_address2"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:AdditionalStreetName"
    xpaths["seller_province"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CountrySubentity"
    xpaths["seller_countrycode"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:Country/cbc:IdentificationCode"
    xpaths["seller_website"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cbc:WebsiteURI"
    xpaths["seller_email"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:ElectronicMail"
    xpaths["seller_cp_city"] = [ "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:PostalZone",
    "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CityName" ]
    xpaths["seller_contact"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Name"
    xpaths["seller_endpoint_id"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cbc:EndpointID"
    xpaths["seller_company_id"] = "/xmlns:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID"
    xpaths["buyer_contactname"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Name"
    xpaths["buyer_phone"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telephone"
    xpaths["buyer_taxcode"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID"
    xpaths["buyer_taxcode_id"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID"
    xpaths["buyer_endpoint_id"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cbc:EndpointID"
    xpaths["buyer_company_id"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID"
    xpaths["buyer_name"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name"
    xpaths["buyer_address"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:StreetName"
    xpaths["buyer_address2"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:AdditionalStreetName"
    xpaths["buyer_province"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CountrySubentity"
    xpaths["buyer_countrycode"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:Country/cbc:IdentificationCode"
    xpaths["buyer_website"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cbc:WebsiteURI"
    xpaths["buyer_reference"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:ID"
    xpaths["buyer_email"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:ElectronicMail"
    xpaths["buyer_cp_city"] = [ "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PostalZone",
    "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CityName" ]
    xpaths["buyer_contact"] = "/xmlns:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Name"
    xpaths["currency"] = "/xmlns:Invoice/cbc:DocumentCurrencyCode"

    xpaths["global_taxes"] = ["/xmlns:Invoice/cac:TaxTotal/cac:TaxSubtotal",
    "/xmlns:Invoice/cac:WithholdingTaxTotal/cac:TaxSubtotal"]
    # relative to global_taxes
    xpaths["gtax_category"] = "cac:TaxCategory/cbc:ID"
    xpaths["gtax_percent"] = "cac:TaxCategory/cbc:Percent"
    xpaths["gtax_name"] = "cac:TaxCategory/cac:TaxScheme/cbc:ID"

    xpaths["invoice_lines"] = "//cac:InvoiceLine"
    # relative to invoice_lines
    xpaths["i_transaction_ref"] = "IssuerTransactionReference" # todo
    xpaths["r_contract_reference"] = "ReceiverContractReference" # todo
    xpaths["line_quantity"] = "cbc:InvoicedQuantity"
    xpaths["line_description"] = ["cac:Item/cbc:Name", "cac:Item/cbc:Description"]
    xpaths["line_price"] = "cac:Price/cbc:PriceAmount"
    xpaths["line_unit"] = "cbc:InvoicedQuantity/@unitCode"
    xpaths["line_taxes"] = ["cac:Item/cac:ClassifiedTaxCategory"]
    xpaths["line_notes"] = ["cbc:Note","cac:Item/cac:SellersItemIdentification/cbc:ID"]
    xpaths["line_code"] = "cac:Item/cac:SellersItemIdentification/cbc:ID"
    xpaths["line_code2"] = "cac:Item/cac:StandardItemIdentification/cbc:ID"
    xpaths["line_code2_scheme"] = "cac:Item/cac:StandardItemIdentification/cbc:ID/@schemeID"
    xpaths["line_discounts"] = "cac:AllowanceCharge/cbc:ChargeIndicator[text()='false']/../../cac:AllowanceCharge"
    xpaths["line_charges"] = "cac:AllowanceCharge/cbc:ChargeIndicator[text()='true']/../../cac:AllowanceCharge"
    xpaths["sequence_number"] = "SequenceNumber" # todo
    xpaths["tax_event_code"] = "SpecialTaxableEvent/SpecialTaxableEventCode" # todo
    xpaths["tax_event_reason"] = "SpecialTaxableEvent/SpecialTaxableEventReason" # todo
    xpaths["delivery_notes"] = "DeliveryNotesReferences/DeliveryNote" # todo
    # relative to invoice_lines/delivery_notes_references/delivery_note
    xpaths["delivery_note_num"] = "DeliveryNoteNumber" # todo

    xpaths["ponumber"] = "/xmlns:Invoice/cac:OrderReference/cbc:ID"
    xpaths["contract_number"] = "/xmlns:Invoice/cac:ContractDocumentReference/cbc:ID"
    # relative to invoice_lines/discounts
    #xpaths["line_discount_percent"] = "cbc:MultiplierFactorNumeric"
    xpaths["line_discount_text"] = "cbc:AllowanceChargeReason"
    xpaths["line_discount_amount"] = "cbc:Amount"
    # relative to invoice_lines/charges
    xpaths["line_charge"] = "cbc:Amount"
    xpaths["line_charge_reason"] = "cbc:AllowanceChargeReason"
    # relative to invoice_lines/taxes
    xpaths["tax_name"] = "cac:TaxScheme/cbc:ID"
    xpaths["tax_category"] = "cbc:ID"
    xpaths["tax_percent"] = "cbc:Percent"

    xpaths["attachments"] = "//cac:AdditionalDocumentReference"
    # relative to attachment
    xpaths["attach_format"] = "cac:Attachment/cbc:EmbeddedDocumentBinaryObject/@mimeCode"
    xpaths["attach_encoding"] = "cac:Attachment/cbc:EmbeddedDocumentBinaryObject/@encodingCode"
    xpaths["attach_description"] = "cbc:DocumentType"
    xpaths["attach_data"] = "cac:Attachment/cbc:EmbeddedDocumentBinaryObject"
    xpaths["attach_filename"] = "cac:Attachment/cbc:EmbeddedDocumentBinaryObject/@filename"

    xpaths["delivery"] = "//cac:Delivery"
    # relative to delivery
    xpaths["delivery_date"] = "cbc:ActualDeliveryDate"
    xpaths["delivery_location_type"] = "cac:DeliveryLocation/cbc:ID/@schemeID"
    xpaths["delivery_location_id"] = "(cac:DeliveryLocation//cbc:ID)[1]"
    xpaths["delivery_address"] = "cac:DeliveryLocation/cac:Address/cbc:StreetName"
    xpaths["delivery_address2"] = "cac:DeliveryLocation/cac:Address/cbc:AdditionalStreetName"
    xpaths["delivery_city"] = "cac:DeliveryLocation/cac:Address/cbc:CityName"
    xpaths["delivery_postalcode"] = "cac:DeliveryLocation/cac:Address/cbc:PostalZone"
    xpaths["delivery_province"] = "cac:DeliveryLocation/cac:Address/cbc:CountrySubentity"
    xpaths["delivery_country"] = "cac:DeliveryLocation/cac:Address/cac:Country/cbc:IdentificationCode"

    xpaths["acharge"] = "/xmlns:Invoice/cac:AllowanceCharge"
    # relative to charge, may be a charge or discount
    xpaths["acharge_indicator"] = "cbc:ChargeIndicator"
    xpaths["acharge_amount"] = "cbc:Amount"
    xpaths["acharge_reason"] = "cbc:AllowanceChargeReason"
    xpaths["acharge_tax_c"] = "cac:TaxCategory/cbc:ID"
    xpaths["acharge_tax_p"] = "cac:TaxCategory/cbc:Percent"
    xpaths["acharge_tax_n"] = "cac:TaxCategory/cac:TaxScheme/cbc:ID"

    return xpaths
