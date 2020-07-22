"""urls for the homepage"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
]
