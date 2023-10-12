import contextlib
from datetime import timedelta
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

from apps.currency.fields import CBRResponse
from apps.currency.utils import CBRProcess


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("last_n_day", type=int, help="Number of days in the past to consider")

    def handle(self, *args: Any, **options: Any) -> str | None:
        days = options["last_n_day"]
        for day_ago in range(days + 1):
            with contextlib.suppress(Exception):
                date = timezone.now().date() - timedelta(days=day_ago)
                cbr_process = CBRProcess()
                if timezone.now().date() == date:
                    result = cbr_process.get_today_currency_rates()
                else:
                    result = cbr_process.get_archive_currency_rates(date)
                cbr_response: CBRResponse = CBRResponse.from_dict(result)
                cbr_process.import_to_db(data=cbr_response)
        self.stdout.write(self.style.SUCCESS("Successfully imported"))
