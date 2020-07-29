"""urls for the homepage"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"), #this stuff is what dictates the URL
    path('contact/', views.contact, name="contact"),
    path('job-listings/', views.job_listings, name="job-listings"),
    path('job-single/', views.job_single, name="job-single"),
    path('post-job/', views.post_job, name="post-job"),
    path('login/', views.login, name="login"),
    path('services/', views.services, name="services"),
    path('service-single/', views.service_single, name="service-single"),
    path('about/', views.about, name="about"),
    

    
]
