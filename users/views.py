from django.shortcuts import render
from users.models import User

#Это вьюшка для авторизации и регистрации


def login(request):
    return render(request, "users/login.html")


def register(request):
    return render(request, "users/register.html")

