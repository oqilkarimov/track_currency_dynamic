from functools import wraps

from apps.currency.exceptions import CBRException


def cbr_success_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        response_json = result.json()
        if result.status_code != 200:
            raise CBRException(response_json)
        return response_json

    return wrapper
