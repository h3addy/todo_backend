from .views import ToDoListCreate
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AppUserCreationForm, AppUserChangeForm
from .models import AppUser, ToDoList


class AppUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = AppUserChangeForm
    model = AppUser
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'avatar', 'spotifyID', 'email', 'accessToken', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('first_name', 'last_name', 'username', 'avatar', 'spotifyID', 'email', 'password1', 'password2', 'accessToken', 'is_staff', 'is_active')}), )
    search_fields = ('username',)
    ordering = ('username',)


class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'completed', 'user')


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(ToDoList, ToDoAdmin)
