import json

from django.http import JsonResponse
from hexbytes import HexBytes


class ResponseStatus:
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


def send_response(data=None, status=ResponseStatus.UNKNOWN, message="N/A", code=200):
    if data is None:
        data = []
    elif isinstance(data, dict):
        data = [data]

    payload = {
        "data": data,
        "status": status.upper(),
        "message": message
    }

    return JsonResponse(payload, status=code)


def sanitize_transaction(tx_details):
    converted_details = {}
    for key, value in tx_details.items():
        if isinstance(value, HexBytes):
            converted_details[key] = value.hex()
        else:
            converted_details[key] = value
    return converted_details
