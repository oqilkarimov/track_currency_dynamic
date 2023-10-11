from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.account.api.v1 import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
]
