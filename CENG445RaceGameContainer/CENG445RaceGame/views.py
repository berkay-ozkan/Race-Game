from CENG445RaceGame.server_integration import communicate_with_server
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from json import dumps


def NotImplemented(*args, **kwargs):
    return HttpResponse("This page is yet to be implemented.")


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
    return redirect("/")


@login_required(login_url="/login")
def repo_create(request: HttpRequest):
    return render(request, "repo-create.html")


@login_required(login_url="/login")
def repo_create_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "create", "parameters": [kwargs]}
    communicate_with_server(request, dumps(command))
    return redirect("/")


@login_required(login_url="/login")
def repo_list(request: HttpRequest):
    command = {"function_name": "list", "parameters": []}
    communicate_with_server(request, dumps(command))
    return redirect("/")


repo_list_attached = NotImplemented
repo_attach = NotImplemented
repo_detach = NotImplemented
repo_delete = NotImplemented
component_factory_list = NotImplemented
component_factory_create = NotImplemented
component_factory_register = NotImplemented
component_factory_unregister = NotImplemented
object_getid = NotImplemented
component_description = NotImplemented
component_type = NotImplemented
component_attributes = NotImplemented
component_draw = NotImplemented
map_getxy = NotImplemented
map_place = NotImplemented
map_view = NotImplemented
map_draw = NotImplemented
car_model = NotImplemented
car_map = NotImplemented
car_driver = NotImplemented
car_pos = NotImplemented
car_angle = NotImplemented
car_topspeed = NotImplemented
car_topfuel = NotImplemented
car_speed = NotImplemented
car_fuel = NotImplemented
