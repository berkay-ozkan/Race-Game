"""
URL configuration for CENG445RaceGame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path
from frontend import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Login pages
    path("login", views.login_view),
    path("login/post", views.login_post),
    path("logout", views.logout_view),
    # Game interface
    path("repo/create", views.repo_create),
    path("repo/create/post", views.repo_create_post),
    path("map/<int:id>", views.game),
    path("map/<int:id>/view", views.map_view),
    path("map/<int:id>/view/post", views.map_view_post)
]
