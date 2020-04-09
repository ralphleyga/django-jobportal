from django.db import models
from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager)
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import PermissionsMixin

MIN_PASSWORD_LENGTH = 7


class AccountManager(BaseUserManager):
    """Restructure Account Base User Manager."""

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model(email=self.normalize_email(email), **kwargs)
        account.set_password(password)
        account.save()
        return account

    def create_staff_user(self, email, password=None, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_staff_user(email, password, **kwargs)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Restructure Abstract Base for Users."""

    email = models.EmailField(unique=True, max_length=255, validators=[MaxLengthValidator(80)])

    first_name = models.CharField(max_length=255, blank=True, validators=[MaxLengthValidator(40)])
    last_name = models.CharField(max_length=255, blank=True, validators=[MaxLengthValidator(40)])

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.email

    def get_short_name(self):
        return self.get_full_name()

    class Meta:
        app_label = 'users'