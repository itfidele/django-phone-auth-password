from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username