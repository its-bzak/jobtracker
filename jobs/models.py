from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class JobPosting(models.Model):
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=1000)
    posted_date = models.DateField(auto_now_add=True)

    employment_type = models.CharField(max_length=50, choices=[
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
    ], default='FT')

    def __str__(self):
        return f"{self.title} at {self.company_name}"

class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE) # Each application is linked to a profile
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE) # Each application is linked to a job posting
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('AP', 'Applied'),
        ('IN', 'Interview'),
        ('OF', 'Offer'),
        ('RE', 'Rejection'),
    ], default='AP')

    def __str__(self):
        return f"{self.job.title} at {self.job.company_name} - {self.applicant.username}"