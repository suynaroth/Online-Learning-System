from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class User(AbstractUser):
    role = models.CharField(max_length=20)

    def save (self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
       return f"{self.username} ({self.role})"