from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import User
from apps.account.types import JWTTokenForUser


class UserController:
    def create_user(self, email: str, password: str) -> User:
        return User.objects.create_user(email=email, password=password)

    def generate_jwt_for_user(self, user: User) -> JWTTokenForUser:
        token = RefreshToken.for_user(user=user)
        return {"refresh": str(token), "access": str(token.access_token)}
