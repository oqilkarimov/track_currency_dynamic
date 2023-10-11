from django.urls import include, path

urlpatterns = [
    path("v1/user/", include("apps.account.api.v1.urls")),
]
