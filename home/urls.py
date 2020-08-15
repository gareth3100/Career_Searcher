"""urls for the homepage"""
from django.urls import path
from . import views
from .views import index
#from .views import ArticleDetails, ArticleAPIView

urlpatterns = [
    path('', views.index, name="index"), #this stuff is what dictates the URL
    path('job-listings/', views.job_listings, name="job-listings"),
    path('job-single/', views.job_single, name="job-single"),
    path('login/', views.login, name="login"),
    path('about/', views.about, name="about"),
    path('saved-jobs/', views.saved_jobs, name="saved-jobs"),
    #path('job-single/', Job_Title) #this is for the url for specific job types when looking things up
    #path('article/', article_list),
    #path('detail/<int:id>/', ArticleDetails.as_view()),
    #path('article/', ArticleAPIView.as_view())

]

