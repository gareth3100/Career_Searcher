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
from .models import SavedJobs
from .forms import SaveThisJob, RemoveThisJob


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

        job_info = {'job_title' : job_title, 'job_area' : job_area, 'job_type' : job_type}

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
        return redirect('/job-listings/?page=1') #need to redirect it but also want to pass in dict as well


def job_listings(request):
    """returns the job-listings page"""
    if request.method == 'GET':
        
        form = SaveThisJob() #adding the checkmark
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
            #del(request.session['context'])
            return render(request, 'job-listings.html', context)

        return render(request, 'job-listings.html', {}) #in the case that it doesn't receive get_data, it just does this

    if 'search_job' in request.POST:
        users = User.objects.all()
        num_users = {'num_users' : len(users)}

        job_title = request.POST['Job_Title']
        job_area = request.POST['Job_Area']
        job_type = request.POST['Job_Type']

        job_info = {'job_title' : job_title, 'job_area' : job_area, 'job_type' : job_type}

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
        return redirect('/job-listings/?page=1') #need to redirect it but also want to pass in dict as well


    elif 'save_job' in request.POST: #save all jobs button at end
        form = SaveThisJob(request.POST)
        if form.is_valid():
            selected_jobs = request.POST.getlist('save') #this one gets all the boxes that are checked
            job_info = []
            saved_job_list = []
            for jobs in selected_jobs: #put all the job values from each checkbox into the list "job_info"
                temp = jobs.split("; ")
                job_info.append(temp)

            counter = 0
            temp2 = []
            final_list = []
            #print(job_info) #not a problem with job_info
            for things in job_info: #big list of all the checked jobs
                for info in things: #checking the info inside the jobs
                    if counter == 1: #checks the city index to see if there is a comma
                        if "," in info:
                            separate_city, separate_state = temp[1].split(", ")
                            temp2.append(separate_city)
                            temp2.append(separate_state)
                        else:
                            temp2.append(info)
                    else:
                        temp2.append(info)
                    counter += 1
                counter = 0 #reset counter for next job

                final_list.append(temp2)
                temp2 = [] #reset list after appending it.

                

            counter = 0
            for jobs in selected_jobs: #grab info from job_info and put them into dictionary
                saved_job_dict = {
                    'job_title' : final_list[counter][0],
                    'job_location' : final_list[counter][1],
                    'job_area' : final_list[counter][2],
                    'company' : final_list[counter][3],
                    'redirect_url' : final_list[counter][5],
                    'job_type' : final_list[counter][4],
                    'has_city' : True
                }
                if saved_job_dict['job_location'] == '':
                    saved_job_dict.clear()
                    saved_job_dict = {
                        'job_title' : final_list[counter][0],
                        'job_area' : final_list[counter][2], #skip the blank one
                        'company' : final_list[counter][3],
                        'redirect_url' : final_list[counter][5], #this and job type mixed up for some reason
                        'job_type' : final_list[counter][4], #no idea why mixed up
                        'has_city' : False
                    }
                saved_job_list.append(saved_job_dict)
                

                if saved_job_list[counter]['has_city']:
                    saved_job_information = SavedJobs(
                        job_title=saved_job_list[counter]['job_title'],
                        job_location=saved_job_list[counter]['job_location'],
                        job_area=saved_job_list[counter]['job_area'],
                        company=saved_job_list[counter]['company'],
                        job_type=saved_job_list[counter]['job_type'],
                        redirect_url=saved_job_list[counter]['redirect_url'],
                        has_city=True
                    )

                    saved_job_information.save()

                    request.user.savedjobs.add(saved_job_information) #this is how you save which user saved the job

                else:
                    saved_job_information = SavedJobs(
                        job_title=saved_job_list[counter]['job_title'],
                        job_area=saved_job_list[counter]['job_area'],
                        company=saved_job_list[counter]['company'],
                        job_type=saved_job_list[counter]['job_type'],
                        redirect_url=saved_job_list[counter]['redirect_url'],
                        has_city=False
                    )

                    saved_job_information.save()

                    request.user.savedjobs.add(saved_job_information)
                
                counter += 1

            temp_next = request.POST.get('next', '/')
            return redirect(temp_next)


def saved_jobs(request):
    """returns the saved-jobs page"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = RemoveThisJob()
            filter_user = SavedJobs.objects.filter(user=request.user).order_by('id') #filters jobs by user that is logged in
            num_objects = filter_user.count()
            paginator = Paginator(filter_user, 10)
            page = request.GET.get('page')
            try:
                job_postings = paginator.get_page(page)
            except PageNotAnInteger:
                job_postings = paginator.page(1)
            except EmptyPage:
                job_postings = paginator.page(paginator.num_pages)

            context = {
                'jobs' : filter_user,
                'count' : num_objects,
                'job_postings' : job_postings,
                'form' : form,
            }

            return render(request, 'saved-jobs.html', context)
        else:
            return render(request, 'saved-jobs.html', {})
        
    elif 'remove_job' in request.POST:
        selected_jobs = request.POST.getlist('remove') #this one gets all the boxes that are checked
        job_info = []
        saved_job_list = []
        for jobs in selected_jobs: #put all the job values from each checkbox into the list "job_info"
            temp = jobs.split("; ")
            job_info.append(temp)

        counter = 0
        temp2 = []
        final_list = []
        for things in job_info: #big list of all the checked jobs
            for info in things: #checking the info inside the jobs
                if counter == 1: #checks the city index to see if there is a comma
                    if "," in info:
                        separate_city, separate_state = temp[1].split(", ")
                        temp2.append(separate_city)
                        temp2.append(separate_state)
                    else:
                        temp2.append(info)
                else:
                    temp2.append(info)
                counter += 1
            counter = 0 #reset counter for next job

            final_list.append(temp2)
            temp2 = [] #reset list after appending it.


        counter = 0
        for jobs in final_list: #grab info from job_info and put them into dictionary
            saved_job_dict = {
                'job_title' : final_list[counter][0],
                'job_location' : final_list[counter][1],
                'job_area' : final_list[counter][2],
                'company' : final_list[counter][3],
                'redirect_url' : final_list[counter][5],
                'job_type' : final_list[counter][4],
                'has_city' : True
            }
            if saved_job_dict['job_location'] == '':
                saved_job_dict.clear()
                saved_job_dict = {
                    'job_title' : final_list[counter][0],
                    'job_area' : final_list[counter][2], #skip the blank one
                    'company' : final_list[counter][3],
                    'redirect_url' : final_list[counter][5], #this and job type mixed up for some reason
                    'job_type' : final_list[counter][4], #no idea why mixed up
                    'has_city' : False
                }
            saved_job_list.append(saved_job_dict)
            counter += 1

        counter = 0
        for jobs in saved_job_list:
            SavedJobs.objects.filter(redirect_url=saved_job_list[counter]['redirect_url']).delete()
            counter += 1
        
        temp_next = request.POST.get('next', '/')
        return redirect(temp_next)

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
