from CENG445RaceGame.server_integration import write_to_backend
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
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_list(request: HttpRequest):
    command = {"function_name": "list", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_list_attached(request: HttpRequest):
    return render(request, "repo-list-attached.html")


@login_required(login_url="/login")
def repo_list_attached_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "list_attached", "parameters": [kwargs]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_attach(request: HttpRequest):
    return render(request, "repo-attach.html")


@login_required(login_url="/login")
def repo_attach_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "attach", "parameters": [kwargs]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_detach(request: HttpRequest):
    return render(request, "repo-detach.html")


@login_required(login_url="/login")
def repo_detach_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "detach", "parameters": [kwargs]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_delete(request: HttpRequest):
    return render(request, "repo-delete.html")


@login_required(login_url="/login")
def repo_delete_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "delete", "parameters": [kwargs]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_factory_list(request: HttpRequest):
    command: dict = {"id": 1, "function_name": "list", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_factory_create(request: HttpRequest):
    return render(request, "component-factory-create.html")


@login_required(login_url="/login")
def component_factory_register(request: HttpRequest):
    return render(request, "component-factory-register.html")


@login_required(login_url="/login")
def component_factory_unregister(request: HttpRequest):
    return render(request, "component-factory-unregister.html")


@login_required(login_url="/login")
def object_getid(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "getid", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_description(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "description", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_type(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "type", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_attributes(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "attributes", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_draw(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "draw", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return render(request, "component-draw.html", context={"reply": reply})


@login_required(login_url="/login")
def map_getxy(request: HttpRequest):
    return render(request, "map-getxy.html")


@login_required(login_url="/login")
def map_place(request: HttpRequest):
    return render(request, "map-place.html")


@login_required(login_url="/login")
def map_view(request: HttpRequest):
    return render(request, "map-view.html")


@login_required(login_url="/login")
def map_draw(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "draw", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    # TODO: Render visuals
    return render(request, "map-draw.html", context={"reply": reply})


@login_required(login_url="/login")
def car_model(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "model", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_map(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "map", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_driver(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "driver", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_pos(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "pos", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_angle(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "angle", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_topspeed(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "topspeed", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_topfuel(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "topfuel", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_speed(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "speed", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_fuel(request: HttpRequest, **kwargs: dict):
    id: int = int(kwargs["id"])
    command = {"id": id, "function_name": "fuel", "parameters": [{}]}
    encoded_reply: bytes = write_to_backend(request, dumps(command))
    reply = encoded_reply.decode()
    return HttpResponse(reply)
