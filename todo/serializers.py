from django.db import models
from rest_framework import serializers
from .models import AppUser, ToDoList


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email', 'spotifyID', 'accessToken',)


class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ('__all__')
