from django.db import models
from django.contrib.auth.models import User #how to input users from database

class SavedJobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savedjobs", null=True)
    job_title = models.CharField(max_length=150, default="")
    job_location = models.CharField(max_length=150, default="")
    job_area = models.CharField(max_length=150, default="")
    company = models.CharField(max_length=150, default="")
    job_type = models.CharField(max_length=150, default="")
    redirect_url = models.CharField(max_length=150, default="")
    has_city = models.CharField(max_length=150, default="")

    def __str__(self):
        return self.job_title
