from django.http import JsonResponse


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
