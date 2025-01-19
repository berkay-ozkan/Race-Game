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
def repo_create(request: HttpRequest):
    return render(request, "repo-create.html")


@login_required(login_url="/login")
def repo_create_post(request: HttpRequest):
    kwargs: dict = request.POST.dict()
    command: dict = {"function_name": "create", "parameters": [kwargs]}
    encoded_reply: str = write_to_backend(request, dumps(command))
    reply = loads(encoded_reply)["result"]
    return HttpResponse(reply)


@login_required(login_url="/login")
def map_view(request: HttpRequest, id: int):
    return render(request, "map-view.html", context={"id": id})


@login_required(login_url="/login")
def map_view_post(request: HttpRequest, id: int):
    kwargs = request.POST.dict()
    command: dict = {
        "type": "map",
        "id": id,
        "function_name": "view",
        "parameters": [kwargs | {
            "user": request.user.username
        }]
    }
    encoded_reply: str = write_to_backend(request, dumps(command))
    reply = loads(encoded_reply)["result"]
    return HttpResponse(reply)


@login_required(login_url="/login")
def game(request: HttpRequest, id: int):
    command: dict = {
        "type": "map",
        "id": id,
        "function_name": "draw",
        "parameters": [{}]
    }
    encoded_reply: str = write_to_backend(request, dumps(command))
    reply = loads(encoded_reply)["result"]
    return render(request,
                  "game.html",
                  context={
                      "id": id,
                      "canvas": dumps(reply[0]),
                      "playerInformation": dumps(reply[1]),
                      "backgroundColor": reply[2],
                      "cellSize": reply[3]
                  })
