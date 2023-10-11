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
