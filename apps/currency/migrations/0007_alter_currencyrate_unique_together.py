# Generated by Django 4.2.6 on 2023-10-11 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("currency", "0006_alter_currencyrate_value"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="currencyrate",
            unique_together={("currency", "rate_date")},
        ),
    ]