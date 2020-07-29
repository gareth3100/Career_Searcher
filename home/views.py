"""Views are used as a function or a class that take a web request and
return a web response. Used to do things such as fetch objects from database
modify those objects if needed, render forms, return HTML """

from django.shortcuts import render
from django.core.mail import send_mail


def index(request):
    """returns the base page"""
    return render(request, 'index.html', {})

def contact(request):
    """returns contact page"""
    if request.method == 'POST': #if they fill a form, they are POSTING info
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        #send an email
        send_mail( #has to be in this specific order
            'message from ' + first_name, #subject
            message, #message
            email, #from email
            ['garethsamadhana@gmail.com'], #to email
        )

        return render(request, 'contact.html', {'first_name' : first_name})
    else:
        return render(request, 'contact.html', {}) #contact/ is under index/ since urls.py RealJobApp has 'index/' in its path first

def job_listings(request):
    """returns the job-listings page"""
    return render(request, 'job-listings.html', {})

def job_single(request):
    """returns the job-single page"""
    return render(request, 'job-single.html', {})

def post_job(request):
    """returns the post-job page"""
    return render(request, 'post-job.html', {})

def login(request):
    """returns the login page"""
    return render(request, 'login.html', {})

def services(request):
    """returns the services page"""
    return render(request, 'services.html', {})

def service_single(request):
    """returns the service-single page"""
    return render(request, 'service-single.html', {})

def about(request):
    """returns the about page"""
    return render(request, 'about.html', {})
