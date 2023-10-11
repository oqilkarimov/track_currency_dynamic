from django.contrib import admin

from apps.currency.models import Currency, CurrencyRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["name", "currency_id", "number_code", "char_code"]
    search_fields = ["name", "char_code"]


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ["currency", "value", "prev_value", "rate_date"]
    date_hierarchy = "rate_date"
