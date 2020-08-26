"""Views are used as a function or a class that take a web request and
return a web response. Used to do things such as fetch objects from database
modify those objects if needed, render forms, return HTML """

import requests
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import ListView
from .forms import MyUserCreationForm
from .models import SavedJobs, Job
from .forms import SaveThisJob


def index(request):
    """returns the base page"""
    users = User.objects.all()
    num_users = {'num_users' : len(users)}
    if request.method == 'GET':
        context = {'num_users' : num_users}
        return render(request, 'index.html', context)

    elif request.method == 'POST':
        job_title = request.POST['Job_Title']
        job_area = request.POST['Job_Area']
        job_type = request.POST['Job_Type']

        job_info = {'job_title' : job_title, 'job_area' : job_area , 'job_type' : job_type}

        if job_type == 'Part Time':
            job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=100&title_only={}&where={}&part_time=1&content-type=application/json'

        if job_type == 'Full Time':
            job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=100&title_only={}&where={}&full_time=1&content-type=application/json'

        job_data = []
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
                'has_city' : True,
                'index' : counter,

                }
                
            except IndexError: #in case they input a state
                job_descriptions = {

                    'job_title' : job_query_result['results'][counter]['title'],
                    'job_area' : job_query_result['results'][counter]['location']['area'][1], #this is the state
                    'creation_date' : job_query_result['results'][counter]['created'],
                    'company' : job_query_result['results'][counter]['company']['display_name'],
                    'redirect_url' : job_query_result['results'][counter]['redirect_url'],
                    'job_description' : job_query_result['results'][counter]['description'],
                    'job_type' : job_query_result['results'][counter]['contract_time'],
                    'has_city' : False,
                    'index' : counter,

                }
            counter += 1 #move on to next job
            job_data.append(job_descriptions) #add all that to a list of dicts we're calling "job_data"
        total_jobs = job_query_result['count']

        context = {'job_data' : job_data, 'total_jobs' : total_jobs, 'num_users' : num_users, 'job_info' : job_info} #shove all dictionaries into here 
        request.session['context'] = context
        return redirect('/job-listings/') #need to redirect it but also want to pass in dict as well


def job_listings(request):
    """returns the job-listings page"""
    if request.method == 'GET':
        form = SaveThisJob()
        get_data = request.session.get('context', False) #returns false if there is no value for 'context'
        if get_data:
            paginator = Paginator(get_data['job_data'], 10)
            page = request.GET.get('page') #this is how we can call the url by typing ?page=1 or ?page=2
            try:
                job_postings = paginator.get_page(page)
            except PageNotAnInteger:
                job_postings = paginator.page(1)
            except EmptyPage:
                job_postings = paginator.page(paginator.num_pages)

            context = {'get_data' : get_data, 'form' : form, 'job_postings' : job_postings}
            del(request.session['context'])
            return render(request, 'job-listings.html', context)

        return render(request, 'job-listings.html', {}) #in the case that it doesn't receive get_data, it just does this

    if request.method == 'POST':
        if 'search_job' in request.POST: #job searching form at top

            job_title = request.POST['Job_Title']
            job_area = request.POST['Job_Area']
            job_type = request.POST['Job_Type']

            if job_type == 'Part Time':
                job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=100&title_only={}&where={}&part_time=1&content-type=application/json'

            if job_type == 'Full Time':
                job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=100&title_only={}&where={}&full_time=1&content-type=application/json'

            job_data = []
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
                    'has_city' : True,
                    'index' : counter,

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
                        'has_city' : False,
                        'index' : counter,

                    }
                counter += 1 #move on to next job
                job_data.append(job_descriptions) #add all that to a list of dicts we're calling "job_data"
            total_jobs = job_query_result['count']


            context = {'job_data' : job_data, 'total_jobs' : total_jobs} #shove all dictionaries into here 
            request.session['context'] = context
            return redirect(request.path) #need to redirect it but also want to pass in dict as well

        elif 'save_job' in request.POST: #save all jobs button at end
            form = SaveThisJob(request.POST)
            if form.is_valid():
                job = form.cleaned_data['Save_job'] #this only gets the last checked box I believe
                selected_jobs = request.POST.getlist('Save_job') #this one gets all the boxes that are checked
                print(selected_jobs) #this prints out ['on', 'on', 'on'] for some reason
                return redirect(request.path)


def saved_jobs(request):
    """returns the saved-jobs page"""
    #user = request.user
    #context = {"user" : user}

    return render(request, 'saved-jobs.html', {}) #in the case that it doesn't receive get_data, it just does this
  

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
    if form.is_valid():
        messages.success(request, "Successfully logged in. Welcome back!")
        return redirect('/') #this is how to change url completely
    return render(request, 'login.html')

def about(request):
    """returns the about page"""
    return render(request, 'about.html', {})
