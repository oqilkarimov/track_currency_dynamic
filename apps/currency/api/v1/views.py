from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.currency.api.v1.serializers import (
    CurrencyAnalyticsQueryParamsSerializer,
    CurrencyAnalyticsResultSerializer,
    CurrencyRateSerializerBase,
    CurrencyRateSerializerForAuthenticated,
    CurrencyThresholdCreateSerializer,
)
from apps.currency.models import Currency, CurrencyRate


class CurrencyRatesAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializerBase
    ordering_fields = ["value"]

    def get_queryset(self):
        today_date = timezone.now().date()
        return CurrencyRate.objects.filter(rate_date__date=today_date)

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            self.serializer_class = CurrencyRateSerializerForAuthenticated
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, context={"user": self.request.user}, many=True)
        return Response(serializer.data)


class CurrencyThresholdCreateViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencyThresholdCreateSerializer


class CurrencyAnalyticsViewSet(GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Currency.objects.all()

    @action(["get"], detail=True)
    def analytics(self, request, *args, **kwargs):
        currency: Currency = self.get_object()
        query_params_serializer = CurrencyAnalyticsQueryParamsSerializer(data=request.query_params)
        query_params_serializer.is_valid(raise_exception=True)
        analytics = Currency.objects.get_analytics_by_giving_period(
            currency=currency, **query_params_serializer.validated_data
        )
        return Response(
            CurrencyAnalyticsResultSerializer(
                analytics,
                many=True,
            ).data
        )
