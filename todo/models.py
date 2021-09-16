from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _

# from .managers import AppUserManager


class AppUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    spotifyID = models.CharField(max_length=50, null=True, blank=True)
    accessToken = models.CharField(max_length=200, null=True, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # objects = AppUserManager

    def __str__(self):
        return self.username


class ToDoList(models.Model):
    user = ForeignKey(AppUser, on_delete=CASCADE, null=True)
    title = models.CharField(max_length=20)
    task = models.CharField(max_length=300)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
