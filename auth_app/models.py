from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import os

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        admin = super().create_superuser(username, email, password, **extra_fields)

        cloud_store_path = '../cloud_store'

        admin_folder_path = os.path.join(cloud_store_path, str(admin.id))
        os.makedirs(admin_folder_path, exist_ok=True)

        # Обновляем поле folder для суперпользователя
        admin.folder = admin.id
        admin.save()

        return admin


class User(AbstractUser):
    folder = models.IntegerField(default=None, null=True)

    objects = CustomUserManager()

