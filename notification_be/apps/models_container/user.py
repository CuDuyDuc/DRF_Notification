from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import  uuid
from notification_be.apps.models_container import UserManager, make_password

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The give email must be set')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.password = make_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise  ValueError('Superuser must have is_superuser = True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active = True.')
        extra_fields.setdefault('role', 'SUPER_ADMIN')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable= True)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=128, blank=True)
    username = models.CharField(max_length=128, null=False, blank=False)
    fullname = models.CharField(max_length=128, null=False, blank=False)
    image = models.ImageField(upload_to='users/', default='image.png')
    is_active = models.BooleanField(default=False, blank=True)
    is_online = models.BooleanField(default=False, blank=True)
    device_token = models.CharField(max_length=255, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    role = models.CharField(max_length=30, null=False, blank=False, default="USER")
    objects = CustomUserManager()