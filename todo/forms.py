from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import AppUser, ToDoList


class AppUserCreationForm(UserCreationForm):

    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class AppUserChangeForm(UserChangeForm):
    class Meta:
        model = AppUser
        fields = ('__all__')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name', 'username', 'email', 'avatar', 'spotifyID')
        exclude = ('password',)


class ToDoListCreateForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'task']


class ToDoListUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'task', 'completed']
