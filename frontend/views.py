from end_to_end_integration import write_to_backend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from json import dumps, loads


def login_view(request):
    return render(request, "login.html")


def login_post(request: HttpRequest):
    username: str = request.POST["username"]

    user = authenticate(username=username, password="")
    if user is None:
        user = User(username=username)
        user.set_password("")
        user.save()

    login(request, user)
    return redirect("/")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("/login")


@login_required(login_url="/login")
def game(request: HttpRequest):
    command: dict = {"function_name": "list_drawables", "parameters": [{}]}
    encoded_reply: str = write_to_backend(request, dumps(command))
    reply: dict = loads(encoded_reply)["result"]
    return render(request, "game.html", context={"map_and_views": reply})
