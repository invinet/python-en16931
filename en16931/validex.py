"""
Module to interact with open.validex.net

You need to create an user at validex.net to be able to
use its API.

"""

import base64
import requests
import time

URL = "https://api2.validex.net/api/validate"


def is_valid_at_validex(invoice, api_key, user_id):
    """Validates an Invoice at open.validex.net

    You need to create an user at validex.net to be able to
    use its API.

    Parameters
    ----------
    api_key: string.
        The authentification API key for validex.net

    user_id: string.
        The user ID of validex.net

    Notes
    -----
    Warnings are not reported.

    """
    payload = {
        'userId': user_id,
        'filename': "{}.xml".format(int(time.time())),
        'fileContents64': base64.b64encode(invoice.to_xml().encode('utf8')),
    }
    headers = {
        'content_type': 'json',
        'accept': 'json',
        'Authorization': "apikey={}".format(api_key),
    }
    response = requests.post(URL, json=payload, headers=headers, verify=False)
    if response.status_code == 200:
        result = response.json()
        if result.get('report') and result['report'].get('result') and\
                result['report']['result'] != 'fatal':
            # Warnings are not reported
            return True
        elif result.get('report') and result['report'].get('id'):
            raise ValueError(_get_validation_errors(result['report']['id']))
        else:
            raise RuntimeError(": ".join(response.json()['error'].values()))
    elif response.status_code == 401:
        raise RuntimeError("Unauthorized: invalid API_KEY")
    else:
        raise RuntimeError(": ".join(response.json()['error'].values()))


def _get_validation_errors(report_id):
    headers = {
        'accept': 'json',
        'Authorization': "apikey={}".format(api_key),
    }
    response = requests.get(
        "{}/{}".format(URL.replace('validate', 'report'), report_id),
        headers=headers,
        verify=False,
    )
    if response.status_code == 200:
        resp = response.json()
        errors = []
        validation_steps = []
        if resp['report'].get('validationSteps'):
            validation_steps.extend(resp['report']['validationSteps'])
        for step in validation_steps:
            if step.get('success') or not step.get('errors'):
                continue
            for error in step['errors']:
                if error.get('message'):
                    errors.add("{}: {}".format(step['description'], error['message']))
                elif error.get('text'):
                    errors.add("{}: {}".format(step['description'], error['text']))
                else:
                    errors.add(str(error))
        return ". ".join(errors)
    elif response.status_code == 401:
        raise RuntimeError("Unauthorized: invalid API_KEY")
    else:
        raise RuntimeError(": ".join(response.json()['error'].values()))
