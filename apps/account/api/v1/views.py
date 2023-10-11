from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.services import UserController

from .serializers import UserRegisterSerializer, UserRetrieveWithTokenSerializer


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_controller = UserController()
        user = user_controller.create_user(**serializer.validated_data)
        return Response(UserRetrieveWithTokenSerializer(user).data)
