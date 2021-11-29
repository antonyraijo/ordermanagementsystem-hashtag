from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager,
    where email is the unique identifier for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create a User with the given email.
        """
        if not email:
            raise ValueError(_("Email is required"))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Super user must have is_superuser=True"))
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Super user must have is_staff=True"))
        return self.create_user(email=email, password=password, **extra_fields)