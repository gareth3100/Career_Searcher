"""urls for the homepage"""
from django.urls import path
from django.contrib.auth import views as auth_views
from home import views as signup_views
from . import views



urlpatterns = [
    path('', views.index, name="index"), #this stuff is what dictates the URL
    path('about/', views.about, name="about"),
    path('saved-jobs/', views.saved_jobs, name="saved-jobs"),
    path('signup/', signup_views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('job-listings/', views.job_listings, name="job-listings"),
    path("<int:id>", views.saved_jobs, name="job-saved"),

]
