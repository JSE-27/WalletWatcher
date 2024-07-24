# WalletWatcher/handler.py

import traceback

from WalletWatcher.utils import send_response, ResponseStatus


class CustomMiddleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return send_response(status=ResponseStatus.FAILED, message='Endpoint Not Found!', code=404)
        elif response.status_code == 405:
            return send_response(status=ResponseStatus.FAILED, message='Method Not Allowed', code=405)
        elif response.status_code == 500:
            return send_response(status=ResponseStatus.FAILED, message='Unable to process the request!', code=400)
        return response


# WalletWatcher/handler.py
def code_exception_handler(exc, _):
    # Capture traceback information
    tb_str = traceback.format_exc()

    print(
        f"\n-----------------Start Exception-----------------\n{tb_str}\n-----------------End Exception-----------------\n")

    return send_response(status=ResponseStatus.FAILED, message=str(exc), code=400)
