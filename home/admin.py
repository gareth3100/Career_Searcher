"""docstring"""
from django.contrib import admin
from django.contrib.auth.models import User
from .forms import MyUserAdmin

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
