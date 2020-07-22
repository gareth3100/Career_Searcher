"""Views are used as a function or a class that take a web request and
return a web response. Used to do things such as fetch objects from database
modify those objects if needed, render forms, return HTML """

from django.shortcuts import render


def index(request):
    """returns the base page"""
    return render(request, 'index.html', {})
