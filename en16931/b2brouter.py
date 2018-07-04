import requests

IMPORT_URL = "https://app.b2brouter.net/projects/{}/invoices/facturae.json"
HALTR_URL = "https://app.b2brouter.net"
IMPORT_URL_TEST = "http://localhost:3001/projects/{}/invoices/facturae.json"
HALTR_URL_TEST = "http://localhost:3001"


def post_to_b2brouter(invoice, api_key, haltr_project_id, test=False):
    payload = invoice.to_xml().encode('utf8')
    import_url = IMPORT_URL.format(haltr_project_id) if not test else \
                 IMPORT_URL_TEST.format(haltr_project_id)
    headers = {
        'content-type': 'application/octet-stream',
        'X-Redmine-API-Key': api_key,
    }
    response = requests.post(import_url, data=payload, headers=headers)
    if response.status_code == 201:
        return response.json()['invoice']['id']
    elif response.status_code == 401:
        raise RuntimeError("Unauthorized: invalid API_KEY")
    else:
        raise RuntimeError("\n".join(response.json()['errors']))
