from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.currency.api.v1.serializers import (
    CurrencyRateSerializerBase,
    CurrencyRateSerializerForAuthenticated,
    CurrencyThresholdCreateSerializer,
)
from apps.currency.models import CurrencyRate


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
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CurrencyThresholdCreateViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencyThresholdCreateSerializer
