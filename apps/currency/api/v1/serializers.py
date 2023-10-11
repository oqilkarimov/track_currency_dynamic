from rest_framework import serializers

from apps.currency.models import CurrencyRate, CurrencyThreshold


class CurrencyRateSerializerBase(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d", source="rate_date")
    charcode = serializers.CharField(source="currency.char_code")

    class Meta:
        model = CurrencyRate
        fields = ("id", "date", "charcode", "value")


class CurrencyRateSerializerForAuthenticated(CurrencyRateSerializerBase):
    is_threshold_exceeded = serializers.SerializerMethodField()

    def get_is_threshold_exceeded(self, currency_rate: CurrencyRate):
        return currency_rate.is_threshold_exceeded_by_giving_user(user=self.context["user"])

    class Meta:
        model = CurrencyRate
        fields = (*CurrencyRateSerializerBase.Meta.fields, "is_threshold_exceeded")


class CurrencyThresholdCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CurrencyThreshold
        fields = ["currency", "threshold", "user"]


class CurrencyAnalyticsQueryParamsSerializer(serializers.Serializer):
    threshold = serializers.DecimalField(max_digits=10, decimal_places=4)
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class CurrencyAnalyticsResultSerializer(CurrencyRateSerializerBase):
    is_threshold_exceeded = serializers.BooleanField(default=False)
    threshold_match_type = serializers.CharField()
    is_max_value = serializers.BooleanField(default=False)
    is_min_value = serializers.BooleanField(default=False)
    percentage_ratio = serializers.SerializerMethodField()

    def get_percentage_ratio(self, currency):
        print(currency.percentage)
        return f"{currency.percentage:.2f}%"

    class Meta:
        model = CurrencyRate
        fields = (
            *CurrencyRateSerializerBase.Meta.fields,
            "is_threshold_exceeded",
            "threshold_match_type",
            "is_max_value",
            "is_min_value",
            "percentage_ratio",
        )
