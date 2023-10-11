from datetime import datetime

import requests
from django.conf import settings

from apps.currency.decorators import cbr_success_response
from apps.currency.fields import CBRResponse
from apps.currency.models import Currency, CurrencyRate


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

    @cbr_success_response
    def get_today_currency_rates(self) -> CBRResponse:
        endpoint = f"{self.BASE_URL}/daily_json.js"
        return requests.get(endpoint, timeout=settings.CBR_DEFAULT_TIMEOUT)

    @cbr_success_response
    def get_archive_currency_rates(self, date: datetime.date) -> CBRResponse:
        endpoint = f"{self.BASE_URL}/archive/{date.year}/{date.month:02d}/{date.day:02d}/daily_json.js"
        return requests.get(endpoint, timeout=settings.CBR_DEFAULT_TIMEOUT)

    def import_to_db(self, data: CBRResponse):
        for valute in data.Valute:
            currency: Currency
            currency, _ = Currency.objects.get_or_create(
                currency_id=valute.ID,
                defaults={
                    "name": valute.Name,
                    "number_code": valute.NumCode,
                    "char_code": valute.CharCode,
                },
            )
            currency_rate = CurrencyRate.objects.create(
                currency=currency,
                value=valute.Value,
                prev_value=valute.Previous,
                prev_rate=currency.get_last_rate(),
                rate_date=data.Date,
            )
            currency.rates.add(currency_rate)  # pylint: disable=no-member
            currency.save()
