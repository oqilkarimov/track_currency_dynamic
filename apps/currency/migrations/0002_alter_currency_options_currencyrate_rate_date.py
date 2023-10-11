# Generated by Django 4.2.6 on 2023-10-11 06:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("currency", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="currency",
            options={"verbose_name": "Currency", "verbose_name_plural": "Currencies"},
        ),
        migrations.AddField(
            model_name="currencyrate",
            name="rate_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]