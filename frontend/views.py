from pickle import loads
from end_to_end_integration import write_to_backend
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
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_list(request: HttpRequest):
    command = {"function_name": "list", "parameters": [{}]}
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_list_attached(request: HttpRequest):
    return render(request, "repo-list-attached.html")


@login_required(login_url="/login")
def repo_list_attached_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "list_attached", "parameters": [kwargs]}
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_attach(request: HttpRequest):
    return render(request, "repo-attach.html")


@login_required(login_url="/login")
def repo_attach_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "attach", "parameters": [kwargs]}
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_detach(request: HttpRequest):
    return render(request, "repo-detach.html")


@login_required(login_url="/login")
def repo_detach_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "detach", "parameters": [kwargs]}
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def repo_delete(request: HttpRequest):
    return render(request, "repo-delete.html")


@login_required(login_url="/login")
def repo_delete_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {"function_name": "delete", "parameters": [kwargs]}
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_factory_list(request: HttpRequest):
    command: dict = {
        "component_factory": True,
        "function_name": "list",
        "parameters": [{}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_factory_create(request: HttpRequest):
    return render(request, "component-factory-create.html")


@login_required(login_url="/login")
def component_factory_create_post(request: HttpRequest):
    component_type_name = request.POST["component_type_name"]
    return redirect(f"/{component_type_name}/create")


@login_required(login_url="/login")
def component_factory_register(request: HttpRequest):
    return render(request, "component-factory-register.html")


@login_required(login_url="/login")
def component_factory_register_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command: dict = {
        "component_factory": True,
        "function_name": "register",
        "parameters": [kwargs]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_factory_unregister(request: HttpRequest):
    return render(request, "component-factory-unregister.html")


@login_required(login_url="/login")
def component_factory_unregister_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command: dict = {
        "component_factory": True,
        "function_name": "unregister",
        "parameters": [kwargs]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def object_getid(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {"id": id, "function_name": "get_id", "parameters": [{}]}
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_description(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "component",
        "id": id,
        "function_name": "description",
        "parameters": [{}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_type(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "component",
        "id": id,
        "function_name": "type",
        "parameters": [{}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_attributes(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "component",
        "id": id,
        "function_name": "attributes",
        "parameters": [{}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def component___setattr__(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    return render(request, "component-__setattr__.html", context={"id": id})


@login_required(login_url="/login")
def component___setattr___post(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    kwargs = request.POST.dict()
    if kwargs["type"] == "int":
        kwargs["value"] = int(kwargs["value"])
    if kwargs["type"] == "float":
        kwargs["value"] = float(kwargs["value"])
    command = {
        "type": "component",
        "id": id,
        "function_name": "__setattr__",
        "parameters": [{
            "name": kwargs["name"],
            "value": kwargs["value"]
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def component_representation(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "component",
        "id": id,
        "function_name": "representation",
        "parameters": [{}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return render(request,
                  "component-representation.html",
                  context={"reply": reply})


@login_required(login_url="/login")
def map___setitem__(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    return render(request, "map-__setitem__.html", context={"id": id})


@login_required(login_url="/login")
def map___setitem___post(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    kwargs = request.POST.dict()
    command = {
        "type":
        "map",
        "id":
        id,
        "function_name":
        "__setitem__",
        "parameters": [{
            "pos": (int(kwargs["y"]), int(kwargs["x"])),
            "id": kwargs["id"]
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def map___delitem__(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    return render(request, "map-__delitem__.html", context={"id": id})


@login_required(login_url="/login")
def map___delitem___post(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    kwargs = request.POST.dict()
    command = {
        "type": "map",
        "id": id,
        "function_name": "__delitem__",
        "parameters": [{
            "pos": (int(kwargs["y"]), int(kwargs["x"]))
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def map_remove(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    return render(request, "map-remove.html", context={"id": id})


@login_required(login_url="/login")
def map_remove_post(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    kwargs = request.POST.dict()
    command = {
        "type": "map",
        "id": id,
        "function_name": "remove",
        "parameters": [{
            "id": kwargs["id"]
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def map_get_y_x(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    return render(request, "map-get-y-x.html", context={"id": id})


@login_required(login_url="/login")
def map_get_y_x_post(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    kwargs = request.POST.dict()
    command: dict = {
        "type": "map",
        "id": id,
        "function_name": "get_y_x",
        "parameters": [kwargs]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def map_place(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    return render(request, "map-place.html", context={"id": id})


@login_required(login_url="/login")
def map_place_post(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    kwargs = request.POST.dict()
    command: dict = {
        "type": "map",
        "id": id,
        "function_name": "place",
        "parameters": [kwargs | {
            "user": request.user.username
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def map_view(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    return render(request, "map-view.html", context={"id": id})


@login_required(login_url="/login")
def map_view_post(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    kwargs = request.POST.dict()
    command: dict = {
        "type": "map",
        "id": id,
        "function_name": "view",
        "parameters": [kwargs]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def map_draw(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "map",
        "id": id,
        "function_name": "draw",
        "parameters": [{}]
    }
    encoded_reply: str = write_to_backend(request, dumps(command))
    reply: tuple = loads(eval(encoded_reply))
    return render(request,
                  "map-draw.html",
                  context={
                      "canvas": reply[0],
                      "all_players_information": reply[1],
                      "bg_color": reply[2],
                      "cell_size": reply[3]
                  })


@login_required(login_url="/login")
def car_create(request: HttpRequest):
    return render(request, "car-create.html")


@login_required(login_url="/login")
def car_create_post(request: HttpRequest):
    kwargs = request.POST.dict()
    command = {
        "type": "car",
        "component_factory": True,
        "function_name": "create",
        "parameters": [kwargs | {
            "component_type_name": "car"
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_model(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_MODEL", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_map(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_MAP", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_driver(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_DRIVER", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_pos(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_position", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_angle(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_angle", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_topspeed(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_MAX_SPEED", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_topfuel(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_MAX_FUEL", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_speed(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_speed", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def car_fuel(request: HttpRequest, **query_parameters: dict):
    id: int = int(query_parameters["id"])
    command = {
        "type": "car",
        "id": id,
        "function_name": "__getattr__",
        "parameters": ["_fuel", {}]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def diagonal_create(request: HttpRequest):
    command = {
        "component_factory": True,
        "function_name": "create",
        "parameters": [{
            "component_type_name": "diagonal"
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def straight_create(request: HttpRequest):
    command = {
        "component_factory": True,
        "function_name": "create",
        "parameters": [{
            "component_type_name": "straight"
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def turn90_create(request: HttpRequest):
    command = {
        "component_factory": True,
        "function_name": "create",
        "parameters": [{
            "component_type_name": "turn90"
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def booster_create(request: HttpRequest):
    command = {
        "component_factory": True,
        "function_name": "create",
        "parameters": [{
            "component_type_name": "booster"
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def fuel_create(request: HttpRequest):
    command = {
        "component_factory": True,
        "function_name": "create",
        "parameters": [{
            "component_type_name": "fuel"
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)


@login_required(login_url="/login")
def rock_create(request: HttpRequest):
    command = {
        "component_factory": True,
        "function_name": "create",
        "parameters": [{
            "component_type_name": "rock"
        }]
    }
    reply: str = write_to_backend(request, dumps(command))
    return HttpResponse(reply)
