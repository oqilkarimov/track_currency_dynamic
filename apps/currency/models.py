from django.db import models
from django.utils import timezone


class Currency(models.Model):
    name = models.CharField(max_length=255, unique=True)
    currency_id = models.CharField(max_length=50, unique=True)
    number_code = models.CharField(max_length=50)
    char_code = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.char_code}/{self.name}"

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class CurrencyRate(models.Model):
    currency = models.ForeignKey("currency.Currency", on_delete=models.CASCADE, related_name="rates")
    value = models.DecimalField(max_digits=6, decimal_places=4)
    prev_value = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    prev_rate = models.ForeignKey(
        "currency.CurrencyRate", on_delete=models.SET_NULL, related_name="next_value", null=True, blank=True
    )
    rate_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.currency.name}/{self.value}"
