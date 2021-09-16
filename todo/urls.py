from django.urls import path
from .views import HomePageView, ToDoListCreate, ToDoListDetails, ToDoListView, ToDoTaskCreate, ToDoTaskDelete, ToDoTaskUpdate, UserDetailsUpdate, UserLoginAPI, UsersList, UserLoginView, UserSignupView, UserDetails
from django.contrib.auth.views import (LogoutView)
from rest_framework.urlpatterns import format_suffix_patterns


app_name = "todo"
urlpatterns = [
    #  user app urls ##################
    # path('', HomePageView.as_view(), name="home"),
    # path('signup/', UserSignupView.as_view(), name="signup"),
    # path('sign_in/', UserLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('update-user/', UserDetailsUpdate.as_view(), name='update-user'),

    # to do app urls ################333
    # path('list-task/', ToDoListCreate.as_view(), name="list-task"),
    # path('create-task/', ToDoTaskCreate.as_view(), name="create-task"),
    # path('update-task/<pk>', ToDoTaskUpdate.as_view(), name="update-task"),
    # path('delete-task/<pk>', ToDoTaskDelete.as_view(), name="delete-task"),


    # APIs
    # path('api-users/', UsersList.as_view(), name='api-users'),
    path('api-users/<username>/', UserDetails.as_view(), name='api-users-details'),
    path('api-user/login/<username>/', UserLoginAPI.as_view(), name='api-user-login'),
    path('api-todos/<user>/', ToDoListView.as_view(), name='api-todos'),
    path('api-todos/<user>/<pk>/', ToDoListDetails.as_view(), name='api-todo-details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
