from django.urls import include, path

from .v1.views import CurrencyRatesAPIView

urlpatterns = [
    path("v1/currency/", include("apps.currency.api.v1.urls")),
    path("v1/rates/", CurrencyRatesAPIView.as_view()),
]
