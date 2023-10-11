from django.urls import path

from apps.currency.api.v1.views import CurrencyThresholdCreateViewSet

urlpatterns = [
    path("user_currency/", CurrencyThresholdCreateViewSet.as_view({"post": "create"})),
]
