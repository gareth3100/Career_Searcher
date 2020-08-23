from django.db import models
from django.contrib.auth.models import User #how to input users from database

class SavedJobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savedjobs", null=True)
    job_title = models.CharField(max_length=50)

    def __str__(self):
        return self.job_title
    
class Job(models.Model):
    saved_jobs = models.ForeignKey(SavedJobs, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    job_location = models.CharField(max_length=50)
    #job_area = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50)
    finished = models.BooleanField()

    def __str__(self):
        return self.company