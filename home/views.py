"""Views are used as a function or a class that take a web request and
return a web response. Used to do things such as fetch objects from database
modify those objects if needed, render forms, return HTML """

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import MyUserCreationForm

def index(request):
    """returns the base page"""

    if request.method == 'POST':

        job_title = request.POST['Job_Title']
        job_area = request.POST['Job_Area']
        job_type = request.POST['Job_Type']

        if job_type == 'Part Time':
            job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=100&title_only={}&where={}&part_time=1&content-type=application/json'

        if job_type == 'Full Time':
            job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=100&title_only={}&where={}&full_time=1&content-type=application/json'

        job_data = []
        counter_dict = {}
        job_query_result = requests.get(job_search_url.format(job_title, job_area)).json() #this has the actual json query result
        counter = 0

        for job in job_query_result['results']:
            try:
                job_descriptions = {

                'job_title' : job_query_result['results'][counter]['title'],
                'job_location' : job_query_result['results'][counter]['location']['area'][3], #this is the city
                'job_area' : job_query_result['results'][counter]['location']['area'][1], #this is the state
                'creation_date' : job_query_result['results'][counter]['created'],
                'company' : job_query_result['results'][counter]['company']['display_name'],
                'redirect_url' : job_query_result['results'][counter]['redirect_url'],
                'job_description' : job_query_result['results'][counter]['description'],
                'job_type' : job_query_result['results'][counter]['contract_time'],
                'has_city' : True

                }
                
            except IndexError: #in case they input a state
                job_descriptions = {

                    'job_title' : job_query_result['results'][counter]['title'],
                    #'job_location' : job_query_result['results'][counter]['location']['area'][3], #this is the city
                    'job_area' : job_query_result['results'][counter]['location']['area'][1], #this is the state
                    'creation_date' : job_query_result['results'][counter]['created'],
                    'company' : job_query_result['results'][counter]['company']['display_name'],
                    'redirect_url' : job_query_result['results'][counter]['redirect_url'],
                    'job_description' : job_query_result['results'][counter]['description'],
                    'job_type' : job_query_result['results'][counter]['contract_time'],
                    'has_city' : False

                }
            counter += 1 #move on to next job
            job_data.append(job_descriptions) #add all that to a list of dicts we're calling "job_data"
        total_jobs = job_query_result['count']


        context = {'job_data' : job_data, 'counter' : counter, 'total_jobs' : total_jobs} #shove all dictionaries into here 
        messages.success(request, {'context': context})
        #request.session['redirect_context'] = context
        #return render(request, 'job-listings.html', context) #can only pass in dicts so that's why we set a dict to job_data
        return redirect('/job-listings/') #need to redirect it but also want to pass in dict as well

    return render(request, 'index.html')


def job_listings(request):
    """returns the job-listings page"""
    if request.method == 'POST':

        job_title = request.POST['Job_Title']
        job_area = request.POST['Job_Area']
        job_type = request.POST['Job_Type']

        if job_type == 'Part Time':
            job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=7&title_only={}&where={}&part_time=1&content-type=application/json'

        if job_type == 'Full Time':
            job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=7&title_only={}&where={}&full_time=1&content-type=application/json'

        job_data = []
        counter_dict = {}
        job_query_result = requests.get(job_search_url.format(job_title, job_area)).json() #this has the actual json query result
        counter = 0

        for job in job_query_result['results']:
            try:
                job_descriptions = {

                    'job_title' : job_query_result['results'][counter]['title'],
                    'job_location' : job_query_result['results'][counter]['location']['area'][3], #this is the city
                    'job_area' : job_query_result['results'][counter]['location']['area'][1], #this is the state
                    'creation_date' : job_query_result['results'][counter]['created'],
                    'company' : job_query_result['results'][counter]['company']['display_name'],
                    'redirect_url' : job_query_result['results'][counter]['redirect_url'],
                    'job_description' : job_query_result['results'][counter]['description'],
                    'job_type' : job_query_result['results'][counter]['contract_time'],
                    'has_city' : True
                }
                
            except IndexError: #in case they input a state
                job_descriptions = {

                    'job_title' : job_query_result['results'][counter]['title'],
                    #'job_location' : job_query_result['results'][counter]['location']['area'][3], #this is the city
                    'job_area' : job_query_result['results'][counter]['location']['area'][1], #this is the state
                    'creation_date' : job_query_result['results'][counter]['created'],
                    'company' : job_query_result['results'][counter]['company']['display_name'],
                    'redirect_url' : job_query_result['results'][counter]['redirect_url'],
                    'job_description' : job_query_result['results'][counter]['description'],
                    'job_type' : job_query_result['results'][counter]['contract_time'],
                    'has_city' : False

                }
            counter += 1 #move on to next job
            job_data.append(job_descriptions) #add all that to a list of dicts we're calling "job_data"
        total_jobs = job_query_result['count']

        context = {'job_data' : job_data, 'counter' : counter, 'total_jobs' : total_jobs} #shove all dictionaries into here 

        return render(request, 'job-listings.html', context) #can only pass in dicts so that's why we set a dict to job_data
    else:

        return render(request, 'job-listings.html')

def signup(request):
    """returns the signup page"""
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sign up successful. Welcome!")
            return redirect('/') #this is how to change url completely
    else:
        form = MyUserCreationForm()
    context = {'form' : form}
    return render(request, 'signup.html', context)

def log_in(request):
    """returns the login page"""
    form = MyUserCreationForm()
    context = {'form' : form}
    messages.success(request, "Successfully logged in. Welcome back!")
    return render(request, 'login.html', context)

def about(request):
    """returns the about page"""
    return render(request, 'about.html', {})

def saved_jobs(request):
    """returns the saved-jobs page"""
    return render(request, 'saved-jobs.html', {})