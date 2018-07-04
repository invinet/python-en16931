import base64
import gzip
import hashlib
import uuid

import requests

WS_URL = "https://ws.b2brouter.com/api/v1/transactions"
IMPORT_URL = "https://app.b2brouter.net/projects/{}/invoices/import.xml"
HALTR_URL = "https://app.b2brouter.net"
WS_URL_TEST = "http://localhost:3000/api/v1/transactions"
IMPORT_URL_TEST = "http://localhost:3001/projects/{}/invoices/import.xml"
HALTR_URL_TEST = "http://localhost:3001"


def post_to_b2brouter(invoice, api_key, haltr_project_id, test=True):
    payload = invoice.to_xml().encode('utf8')
    import_url = IMPORT_URL.format(haltr_project_id) if not test else \
                 IMPORT_URL_TEST.format(haltr_project_id)
    request = {
        'id': "{}".format(hashlib.md5(payload).hexdigest()),
        'haltr_url': HALTR_URL if not test else HALTR_URL_TEST,
        'import_url': import_url,
        'process': 'Haltr::ImportXml',
        'api_key': api_key,
        'payload_filename': "{}.xml".format(uuid.uuid4()),
        'payload': compress(payload),
    }
    params = {
        'transaction': request,
        'token': api_key
    }
    ws_url = WS_URL if not test else WS_URL_TEST
    response = requests.post(ws_url, json=params)
    if response.status_code == 200:
        return response.json['id']
    else:
        raise RuntimeError(response.json['message'])


def compress(payload):
    if payload is None:
        return None
    buf = gzip.compress(payload)
    return base64.b64encode(buf)
