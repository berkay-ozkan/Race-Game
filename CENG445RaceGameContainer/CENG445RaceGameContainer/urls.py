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
    path('repo/list-attached', views.NotImplemented),
    path('repo/attach', views.NotImplemented),
    path('repo/detach', views.NotImplemented),
    path('repo/delete', views.NotImplemented),
    path('component-factory/list', views.NotImplemented),
    path('component-factory/create', views.NotImplemented),
    path('component-factory/register', views.NotImplemented),
    path('component-factory/unregister', views.NotImplemented),
    path('object/<int:id>/getid', views.NotImplemented),
    path('component/<int:id>/description', views.NotImplemented),
    path('component/<int:id>/type', views.NotImplemented),
    path('component/<int:id>/attributes', views.NotImplemented),
    path('component/<int:id>/__getattr__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('component/<int:id>/__setattr__',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('component/<int:id>/draw', views.NotImplemented),
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
    path('map/<int:id>/getxy', views.NotImplemented),
    path('map/<int:id>/place', views.NotImplemented),
    path('map/<int:id>/view', views.NotImplemented),
    path('map/<int:id>/draw', views.NotImplemented),
    path('cell/<int:id>/interact',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/model', views.NotImplemented),
    path('car/<int:id>/map', views.NotImplemented),
    path('car/<int:id>/driver', views.NotImplemented),
    path('car/<int:id>/pos', views.NotImplemented),
    path('car/<int:id>/angle', views.NotImplemented),
    path('car/<int:id>/topspeed', views.NotImplemented),
    path('car/<int:id>/topfuel', views.NotImplemented),
    path('car/<int:id>/speed', views.NotImplemented),
    path('car/<int:id>/fuel', views.NotImplemented),
    path('car/<int:id>/start',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/stop',
         views.NotImplemented),  # TODO: Should this be accessible?
    path('car/<int:id>/accelerate', views.NotImplemented),
    path('car/<int:id>/decelerate', views.NotImplemented),
    path('car/<int:id>/left', views.NotImplemented),
    path('car/<int:id>/right', views.NotImplemented),
    path('car/<int:id>/tick',
         views.NotImplemented),  # TODO: Should this be accessible?
]
