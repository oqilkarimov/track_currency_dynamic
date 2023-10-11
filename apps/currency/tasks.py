from celery import shared_task

from apps.currency.utils import CBRProcess, CBRResponse


@shared_task
def task_daily_import_currency_rate():
    cbr_process = CBRProcess()
    cbr_resp = CBRResponse.from_dict(cbr_process.get_today_currency_rates())
    cbr_process.import_to_db(data=cbr_resp)
