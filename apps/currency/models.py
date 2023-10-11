from django.db import models
from django.db.models import (
    BooleanField,
    Case,
    ExpressionWrapper,
    F,
    FloatField,
    Manager,
    Max,
    Min,
    Q,
    Value,
    When,
)
from django.utils import timezone

from apps.account.models import User


class CurrencyRate(models.Model):
    currency = models.ForeignKey("currency.Currency", on_delete=models.CASCADE, related_name="rates")
    value = models.DecimalField(max_digits=10, decimal_places=4)
    prev_value = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    prev_rate = models.ForeignKey(
        "currency.CurrencyRate", on_delete=models.SET_NULL, related_name="next_value", null=True, blank=True
    )
    rate_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.currency.name}/{self.value}"

    def is_threshold_exceeded_by_giving_user(self, user: User) -> bool:
        if user_threshold := user.currency_thresholds.filter(currency=self.currency).first():
            return self.value > user_threshold.threshold
        return False

    class Meta:
        ordering = ["-rate_date"]
        unique_together = ["currency", "rate_date"]


class CurrencyThreshold(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="currency_thresholds")
    threshold = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.ForeignKey("currency.Currency", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["currency", "user"]


class CurrencyAnalyticsManager(Manager):
    def get_analytics_by_giving_period(self, currency, threshold, date_from, date_to):
        rates_by_giving_period_for = CurrencyRate.objects.filter(
            currency=currency, rate_date__date__gte=date_from, rate_date__date__lte=date_to
        )
        max_min_values_in_query = rates_by_giving_period_for.aggregate(
            max_value=Max("value"), min_value=Min("value")
        )
        return rates_by_giving_period_for.annotate(
            is_threshold_exceeded=ExpressionWrapper(Q(value__gte=threshold), output_field=BooleanField()),
            threshold_match_type=Case(
                When(value__gt=threshold, then=Value("greater")),
                When(value__lt=threshold, then=Value("less")),
                When(value=threshold, then=Value("equal")),
            ),
            is_max_value=ExpressionWrapper(
                Q(value=max_min_values_in_query["max_value"]), output_field=BooleanField()
            ),
            is_min_value=ExpressionWrapper(
                Q(value=max_min_values_in_query["min_value"]), output_field=BooleanField()
            ),
            percentage=ExpressionWrapper(100 * F("value") / threshold, output_field=FloatField()),
        )


class Currency(models.Model):
    name = models.CharField(max_length=255, unique=True)
    currency_id = models.CharField(max_length=50, unique=True)
    number_code = models.CharField(max_length=50)
    char_code = models.CharField(max_length=50, unique=True)

    objects = CurrencyAnalyticsManager()

    def __str__(self) -> str:
        return f"{self.char_code}/{self.name}"

    def get_last_rate(self) -> CurrencyRate:
        return self.rates.first()  # pylint: disable=no-member

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
