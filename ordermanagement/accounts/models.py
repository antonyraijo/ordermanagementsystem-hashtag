from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from accounts.managers import CustomUserManager


# custom user model
class CustomUser(AbstractUser):

    username = None

    name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    is_consumer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return "{}-{}".format(self.name, self.email)


# to create token for every user objects when user object creation time
@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)