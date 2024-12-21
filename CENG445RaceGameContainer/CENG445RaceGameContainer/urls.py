"""
URL configuration for CENG445RaceGameContainer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CENG445RaceGame import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Login pages
    path('login', views.login_view),
    path('login/post', views.login_post),
    path('logout', views.logout_view),
    # Game interface
    # TODO: Check code for functions I've missed
    path('repo/create', views.repo_create),
    path('repo/create/post', views.repo_create_post),
    path('repo/list', views.repo_list),
    path('repo/list-attached', views.repo_list_attached),
    path('repo/list-attached/post', views.repo_list_attached_post),
    path('repo/attach', views.repo_attach),
    path('repo/attach/post', views.repo_attach_post),
    path('repo/detach', views.repo_detach),
    path('repo/detach/post', views.repo_detach_post),
    path('repo/delete', views.repo_delete),
    path('component-factory/list', views.component_factory_list),
    path('component-factory/create', views.component_factory_create),
    path('component-factory/register', views.component_factory_register),
    path('component-factory/unregister', views.component_factory_unregister),
    path('object/<int:id>/getid', views.object_getid),
    path('component/<int:id>/description', views.component_description),
    path('component/<int:id>/type', views.component_type),
    path('component/<int:id>/attributes', views.component_attributes),
    path('component/<int:id>/__getattr__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('component/<int:id>/__setattr__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('component/<int:id>/draw', views.component_draw),
    path('map/<int:id>/__init__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('map/<int:id>/__getitem__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('map/<int:id>/__setitem__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('map/<int:id>/__delitem__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('map/<int:id>/remove',
         views.NotImplemented),  # TODO: This requires an object reference
    path('map/<int:id>/getxy', views.map_getxy),
    path('map/<int:id>/place', views.map_place),
    path('map/<int:id>/view', views.map_view),
    path('map/<int:id>/draw', views.map_draw),
    path('cell/<int:id>/interact',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/model', views.car_model),
    path('car/<int:id>/map', views.car_map),
    path('car/<int:id>/driver', views.car_driver),
    path('car/<int:id>/pos', views.car_pos),
    path('car/<int:id>/angle', views.car_angle),
    path('car/<int:id>/topspeed', views.car_topspeed),
    path('car/<int:id>/topfuel', views.car_topfuel),
    path('car/<int:id>/speed', views.car_speed),
    path('car/<int:id>/fuel', views.car_fuel),
    path('car/<int:id>/start',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/stop',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/accelerate',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/decelerate',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/left',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/right',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/tick',
         views.NotImplemented),  # TODO: Should this be accessible?
]
