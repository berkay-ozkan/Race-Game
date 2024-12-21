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
    path('repo/delete/post', views.repo_delete_post),
    path('component-factory/list', views.component_factory_list),
    path('component-factory/create', views.component_factory_create),
    path('component-factory/create/post', views.component_factory_create_post),
    path('component-factory/register', views.component_factory_register),
    path('component-factory/register/post',
         views.component_factory_register_post),
    path('component-factory/unregister', views.component_factory_unregister),
    path('component-factory/unregister/post',
         views.component_factory_unregister_post),
    path('object/<int:id>/getid', views.object_getid),
    path('component/<int:id>/description', views.component_description),
    path('component/<int:id>/type', views.component_type),
    path('component/<int:id>/attributes', views.component_attributes),
    path('component/<int:id>/__getattr__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('component/<int:id>/__setattr__', views.component___setattr__),
    path('component/<int:id>/__setattr__/post',
         views.component___setattr___post),
    path('component/<int:id>/representation', views.component_representation),
    path('map/<int:id>/__getitem__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('map/<int:id>/__setitem__', views.map___setitem__),
    path('map/<int:id>/__setitem__/post', views.map___setitem___post),
    path('map/<int:id>/__delitem__', views.map___delitem__),
    path('map/<int:id>/__delitem__/post', views.map___delitem___post),
    path('map/<int:id>/remove', views.map_remove),
    path('map/<int:id>/remove/post', views.map_remove_post),
    path('map/<int:id>/get-y-x', views.map_get_y_x),
    path('map/<int:id>/get-y-x/post', views.map_get_y_x_post),
    path('map/<int:id>/place', views.map_place),
    path('map/<int:id>/place/post', views.map_place_post),
    path('map/<int:id>/view', views.map_view),
    path('map/<int:id>/view/post', views.map_view_post),
    path('map/<int:id>/draw', views.map_draw),
    path('cell/<int:id>/interact',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/create', views.car_create),
    path('car/create/post', views.car_create_post),
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
    path('diagonal/create', views.diagonal_create),
    path('straight/create', views.straight_create),
    path('turn90/create', views.turn90_create),
    path('booster/create', views.booster_create),
    path('fuel/create', views.fuel_create),
    path('rock/create', views.rock_create),
]
