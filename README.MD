## Run the web service using Docker

```bash
docker-compose up --build -d
```

## Create superuser

```bash
docker-compose exec currency_app python manage.py createsuperuser
```

## Import initial rates from CBR service

```bash
docker-compose exec currency_app python manage.py cbr_import 30
```

## Configure periodic task for daily fetch rates

1. Go to Admin Panel /admin/django_celery_beat/periodictask
2. Create periodic task with registered task apps.currency.tasks.task_daily_import_currency_rate
3. Set crontab
4. Save it
