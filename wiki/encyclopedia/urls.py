from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new/", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("randompage/", views.random, name="random"),
]
