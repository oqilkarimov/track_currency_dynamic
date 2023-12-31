# Generated by Django 4.2.6 on 2023-10-11 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("currency", "0002_alter_currency_options_currencyrate_rate_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currencyrate",
            name="prev_rate",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="next_value",
                to="currency.currencyrate",
            ),
        ),
        migrations.AlterField(
            model_name="currencyrate",
            name="prev_value",
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True),
        ),
    ]
