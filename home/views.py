"""Views are used as a function or a class that take a web request and
return a web response. Used to do things such as fetch objects from database
modify those objects if needed, render forms, return HTML """

from django.shortcuts import render
from django.core.mail import send_mail
import requests
#import clearbit


def index(request):
    """returns the base page"""
    #clearbit.key = 'sk_76afcd60f04d489deff2396d86e9b9e7'

    if request.method == 'POST':

        job_title = request.POST['Job_Title']
        job_area = request.POST['Job_Area']
        job_type = request.POST['Job_Type']

        if job_type == 'Part Time':
            job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=7&title_only={}&where={}&part_time=1&content-type=application/json'

        if job_type == 'Full Time':
            job_search_url = 'https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=89169241&app_key=9730280226cca44dbc8fb53ce085e104&results_per_page=7&title_only={}&where={}&full_time=1&content-type=application/json'

        job_data = []
        logo_data = []
        counter_dict = {}
        job_query_result = requests.get(job_search_url.format(job_title, job_area)).json() #this has the actual json query result
        counter = 0

        for job in job_query_result['results']:
            job_descriptions = {

                'job_title' : job_query_result['results'][counter]['title'],
                'job_location' : job_query_result['results'][counter]['location']['area'][3],
                'job_area' : job_query_result['results'][counter]['location']['area'][1],
                'creation_date' : job_query_result['results'][counter]['created'],
                'company' : job_query_result['results'][counter]['company']['display_name'],
                'redirect_url' : job_query_result['results'][counter]['redirect_url'],
                'job_description' : job_query_result['results'][counter]['description'],
                'job_type' : job_query_result['results'][counter]['contract_time'],

            }
            counter += 1 #move on to next job
            job_data.append(job_descriptions) #add all that to a list of dicts we're calling "job_data"
        
            '''company_logo_url = 'https://company.clearbit.com/v1/domains/find?name={}'
            logo_query_result = requests.get(company_logo_url.format(job_descriptions['company'])).json()
            print(logo_query_result)

        counter2 = 0
        for logo in logo_query_result:
            
            logo_image = {
                'image' : logo_query_result[counter2]['logo']
            }
            logo_data.append(logo_image)

            counter2 += 1
        
        logo_context = {'logo_data' : logo_data}
        print(logo_context)'''

        context = {'job_data' : job_data, 'counter' : counter} #shove all dictionaries into here 

        #return render(request, 'job-listings.html', job_context, logo_context)
        return render(request, 'job-listings.html', context) #can only pass in dicts so that's why we set a dict to job_data

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
        logo_data = []
        counter_dict = {}
        job_query_result = requests.get(job_search_url.format(job_title, job_area)).json() #this has the actual json query result
        counter = 0

        for job in job_query_result['results']:
            job_descriptions = {

                'job_title' : job_query_result['results'][counter]['title'],
                'job_location' : job_query_result['results'][counter]['location']['area'][3],
                'job_area' : job_query_result['results'][counter]['location']['area'][1],
                'creation_date' : job_query_result['results'][counter]['created'],
                'company' : job_query_result['results'][counter]['company']['display_name'],
                'redirect_url' : job_query_result['results'][counter]['redirect_url'],
                'job_description' : job_query_result['results'][counter]['description'],
                'job_type' : job_query_result['results'][counter]['contract_time'],

            }
            counter += 1 #move on to next job
            job_data.append(job_descriptions) #add all that to a list of dicts we're calling "job_data"
        
            '''company_logo_url = 'https://company.clearbit.com/v1/domains/find?name={}'
            logo_query_result = requests.get(company_logo_url.format(job_descriptions['company'])).json()
            print(logo_query_result)

        counter2 = 0
        for logo in logo_query_result:
            
            logo_image = {
                'image' : logo_query_result[counter2]['logo']
            }
            logo_data.append(logo_image)

            counter2 += 1
        
        logo_context = {'logo_data' : logo_data}
        print(logo_context)'''

        context = {'job_data' : job_data, 'counter' : counter} #shove all dictionaries into here 

        #return render(request, 'job-listings.html', job_context, logo_context)
        return render(request, 'job-listings.html', context) #can only pass in dicts so that's why we set a dict to job_data

    return render(request, 'index.html')

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