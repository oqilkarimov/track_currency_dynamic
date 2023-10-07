from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a new user with the given email and password.

        Validates that the email is provided.
        Normalizes the email and sets it on a new user instance.
        Sets the password and saves the user.

        Args:
           email: The email address for the new user.
           password: The password for the new user.
           extra_fields: Any additional fields for the user.

        Returns:
           The newly created user object.

        Raises:
           ValueError: If no email is provided."""

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a superuser with the given email and password.

        Sets is_staff, is_superuser, and is_active to True by default.
        Validates that is_staff and is_superuser are True.

        Args:
           email: Email address for the superuser.
           password: Password for the superuser.
           extra_fields: Additional fields for the superuser.

        Returns:
           The newly created superuser object.

        Raises:
           ValueError: If is_staff or is_superuser are not True."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
