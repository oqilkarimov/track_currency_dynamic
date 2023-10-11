from rest_framework import serializers

from apps.currency.models import CurrencyRate


class CurrencyRateSerializerBase(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d", source="rate_date")
    charcode = serializers.CharField(source="currency.char_code")

    class Meta:
        model = CurrencyRate
        fields = ("id", "date", "charcode", "value")


class CurrencyRateSerializerForAuthenticated(CurrencyRateSerializerBase):
    is_threshold_exceeded = serializers.BooleanField(default=False)

    class Meta:
        model = CurrencyRate
        fields = (*CurrencyRateSerializerBase.Meta.fields, "is_threshold_exceeded")
