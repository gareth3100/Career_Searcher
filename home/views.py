"""Views are used as a function or a class that take a web request and
return a web response. Used to do things such as fetch objects from database
modify those objects if needed, render forms, return HTML """

from django.shortcuts import render
from django.core.mail import send_mail
import requests
from django.http import HttpResponse, JsonResponse

def index(request):
    """returns the base page"""
    if request.method == 'POST':

        job_title = request.POST['Job_Title']
        job_area = request.POST['Job_Area']
        job_type = request.POST['Job_Type']

        job_search = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=7&what={}&where={}&content-type=application/json'

        for jobs_retrieved in job_search:

            query_result = requests.get(job_search.format(job_title, job_area)).json()
            counter = 0
            job_descriptions = { #there are inconsistencies so if for example 'contract_time' is not present in json, it gives error
            #need to make some if statements in the html files for certain job characteristics

                'job_title' : query_result['results'][counter]['title'],
                'job_location' : query_result['results'][counter]['location']['area'][3],
                'job_area' : query_result['results'][counter]['location']['area'][1],
                'creation_date' : query_result['results'][counter]['created'],
                'company' : query_result['results'][counter]['company']['display_name'],
                'redirect_url' : query_result['results'][counter]['redirect_url'],
                'job_description' : query_result['results'][counter]['description'],

            }

            context = {'job_descriptions' : job_descriptions}
            counter += 1
            return render(request, 'job-listings.html', context)

        #GET https://autocomplete.clearbit.com/v1/companies/suggest?query={} #this is for company logo, just change :name to title

    return render(request, 'index.html')
    
def job_listings(request):
    """returns the job-listings page"""
    if request.method == 'POST':

        job_title = request.POST['Job_Title'],
        job_area = request.POST['Job_Area'],
        job_type = request.POST['Job_Type'],

        base_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=7&what={}&where={}'
        temp = requests.get(base_url.format(job_title, job_area)).json()

    return render(request, 'job-listings.html')

def job_single(request):
    """returns the job-single page"""
    return render(request, 'job-single.html', {})

def login(request):
    """returns the login page"""
    return render(request, 'login.html', {})

def about(request):
    """returns the about page"""
    return render(request, 'about.html', {})

def saved_jobs(request):
    """returns the saved-jobs page"""
    return render(request, 'saved-jobs.html', {})