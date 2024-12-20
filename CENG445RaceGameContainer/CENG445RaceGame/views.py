from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def login_view(request):
    return render(request, 'login.html')


def login_post(request: HttpRequest):
    username: str = request.POST['username']

    user = authenticate(username=username, password="")
    if user is None:
        user = User(username=username)
        user.set_password("")
        user.save()

    login(request, user)
    return redirect("/")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("/")


def NotImplemented(*args, **kwargs):
    return HttpResponse("This page is yet to be implemented.")
