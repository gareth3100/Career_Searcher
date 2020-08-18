"""urls for the homepage"""
from django.urls import path
from . import views
from .views import index
#from .views import ArticleDetails, ArticleAPIView

urlpatterns = [
    path('', views.index, name="index"), #this stuff is what dictates the URL
    path('job-listings/', views.job_listings, name="job-listings"),
    path('login/', views.login, name="login"),
    path('about/', views.about, name="about"),
    path('saved-jobs/', views.saved_jobs, name="saved-jobs"),

]

