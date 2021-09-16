from re import T
from django.db.models import manager
from django.forms.models import construct_instance
from django.http.response import Http404, HttpResponseForbidden
from .serializers import AppUserSerializer, ToDoListSerializer
from rest_framework import serializers
from .models import AppUser, ToDoList
from .forms import AppUserCreationForm, UserUpdateForm, ToDoListCreateForm, ToDoListUpdateForm
from django.shortcuts import reverse
from django.views import generic
from django.contrib.auth.views import (LoginView)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import generateAccessToken
import json

# USER CRUD APP #######################33


class HomePageView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class UserSignupView(generic.CreateView):
    form_class = AppUserCreationForm
    template_name = "signup.html"

    def get_success_url(self) -> str:
        return reverse("app_users:login")


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self) -> str:
        url = "/"
        return url


class UserDetailsUpdate(LoginRequiredMixin, generic.UpdateView):
    login_url = '/sign_in/'
    redirect_field_name = 'redirect_to'
    template_name = "user_profile.html"
    form_class = UserUpdateForm
    success_url = "/"

    def get_object(self):
        return self.request.user

#######################################################


# TO DO CRUD APP ######################333
class ToDoListCreate(LoginRequiredMixin, generic.ListView):
    login_url = "/sign_in/"
    template_name = "todo.html"
    model = ToDoList

    def get_context_data(self, **kwargs):
        print(self.request.user)
        context = super().get_context_data(**kwargs)
        # tasks = self.model.objects.all()
        tasks = self.model.objects.filter(user=self.request.user)
        context.update({
            "tasks": tasks,
        })
        return context


class ToDoTaskCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/sign_in/"
    template_name = "todo.html"
    form_class = ToDoListCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "button": "Create",
        })
        return context

    def get_success_url(self) -> str:
        url = "/list-task"
        return url


class ToDoTaskUpdate(LoginRequiredMixin, generic.UpdateView):
    login_url = "/sign_in/"
    template_name = "todo.html"
    form_class = ToDoListUpdateForm
    model = ToDoList

    def get_queryset(self):
        queryset = self.model.objects.filter(pk=self.kwargs['pk'], user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "button": "Update",
        })
        return context

    def get_success_url(self) -> str:
        url = "/list-task"
        return url


class ToDoTaskDelete(LoginRequiredMixin, generic.DeleteView):
    login_url = "/sign_in/"
    model = ToDoList
    template_name = "todolist_confirm_delete.html"

    def get_success_url(self) -> str:
        url = "/list-task"
        return url

#################################################################

# APIs


class UsersList(APIView):
    def get(self, request, format=None):
        # users = AppUser.objects.all()
        # serializer = AppUserSerializer(users, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        accessToken = generateAccessToken()
        new_user = request.data
        new_user.update({
            "accessToken": str(accessToken)
        })
        serializer = AppUserSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(APIView):
    def get_object(self, request, username):
        try:
            new_data = json.loads(request.body)
            inputAccessToken = new_data['accessToken']
            userObject = AppUser.objects.get(username=username)
            if userObject.accessToken == inputAccessToken:
                return userObject
            return None
        except:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(request, username)
        serializer = AppUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):
        user = self.get_object(request, username)
        # print(user is None)
        # print(request.data)
        if user is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = AppUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        user = self.get_object(request, username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginAPI(APIView):
    def get_object(self, request, username):
        try:
            return AppUser.objects.get(username=username)
        except:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(request, username)
        try:
            if request.GET['password'] is not None:
                password = request.GET['password']
                if password != user.password:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass
        serializer = AppUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

############# TO DO API ###################################


class ToDoListView(APIView):
    def get(self, request, user, format=None):
        try:
            inputAccessToken = request.GET['accessToken']
            userObject = AppUser.objects.get(accessToken=inputAccessToken)
            if str(userObject.id) == user:
                tasks = ToDoList.objects.filter(user=user)
                serializer = ToDoListSerializer(tasks, many=True)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user, format=None):
        try:
            request.data['title']
            request.data['task']
            if request.data['title'] == '' or request.data['task'] == '':
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            inputAccessToken = request.GET['accessToken']
            userObject = AppUser.objects.get(accessToken=inputAccessToken)
            if str(userObject.id) == user:
                task = request.data
                task.update({
                    "user": user,
                })
                # print(task)
                serializer = ToDoListSerializer(data=task)
                if serializer.is_valid():
                    serializer.save()
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user, format=None):
        # print(request.GET)
        try:
            inputAccessToken = request.GET['accessToken']
            userObject = AppUser.objects.get(accessToken=inputAccessToken)
            if str(userObject.id) == user:
                tasks = ToDoList.objects.filter(user=user)
                # serializer = ToDoListSerializer(tasks, many=True)
                tasks.delete()
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToDoListDetails(APIView):
    def get_object(self, request, user, pk):
        try:
            # print(json.loads(request.body))
            new_data = json.loads(request.body)
            inputAccessToken = new_data['accessToken']
            userObject = AppUser.objects.get(accessToken=inputAccessToken)
            if str(userObject.id) == user:
                return ToDoList.objects.get(pk=pk, user=user)
            else:
                return Response(status.HTTP_403_FORBIDDEN)
        except:
            raise Http404

    def get(self, request, user, pk, format=None):
        task = self.get_object(request, user, pk)
        serializer = ToDoListSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user, pk, format=None):
        # try:
        #     request.data['title']
        #     request.data['task']
        # except:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        task = self.get_object(request, user, pk)
        serializer = ToDoListSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user, pk, format=None):
        task = self.get_object(request, user, pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
