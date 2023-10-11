from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.account.models import User
from apps.account.services import UserController
from apps.account.types import JWTTokenForUser


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password_confirmation = serializers.CharField()

    def validate_email(self, email: str):
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists!")
        return email

    def validate_password(self, password: str):
        if password != self.initial_data["password_confirmation"]:
            raise ValidationError("Password mismatch!")
        return password

    def validate(self, attrs):
        attrs.pop("password_confirmation")
        return attrs


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class UserRetrieveWithTokenSerializer(UserRetrieveSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, user: User) -> JWTTokenForUser:
        user_controller = UserController()
        return user_controller.generate_jwt_for_user(user=user)

    class Meta:
        model = User
        fields = [*UserRetrieveSerializer.Meta.fields, "token"]
