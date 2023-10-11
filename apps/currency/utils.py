from datetime import datetime

import requests
from django.conf import settings

from apps.currency.fields import CBRResponse


class CBRProcess:
    """Gets currency rates from the CBR API.
    Fetches current and historical rates.

    Methods:
     get_today_currency_rates: Gets current rates.
     get_archive_currency_rates: Gets historical rates for a date.

    Args:
     date: The date to get historical rates for.

    Returns:
     CBRResponse: The API response object.
    """

    BASE_URL = settings.CBR_BASE_URL

    def get_today_currency_rates(self) -> CBRResponse:
        endpoint = f"{self.BASE_URL}/daily_json.js"
        response = requests.get(endpoint, timeout=settings.CBR_DEFAULT_TIMEOUT)
        return response.json()

    def get_archive_currency_rates(self, date: datetime.date) -> CBRResponse:
        endpoint = f"{self.BASE_URL}/archive/{date.year}/{date.month}/{date.day}/daily_json.js"
        response = requests.get(endpoint, timeout=settings.CBR_DEFAULT_TIMEOUT)
        return response.json()
