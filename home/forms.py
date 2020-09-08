from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SaveThisJob(forms.Form):
    Save_job = forms.BooleanField(required=False)

class RemoveThisJob(forms.Form):
    Remove_job = forms.BooleanField(required=False)

