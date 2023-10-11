from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.currency.api.v1.views import CurrencyAnalyticsViewSet, CurrencyThresholdCreateViewSet

router = DefaultRouter()
router.register("", CurrencyAnalyticsViewSet)

urlpatterns = [
    path("user_currency/", CurrencyThresholdCreateViewSet.as_view({"post": "create"})),
]

urlpatterns += router.urls
