from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20)
    profile_status = models.CharField(max_length=20, default='incomplete')
    created_at = models.DateTimeField(auto_now_add=True)

class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    verified = models.BooleanField(default=False)

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    experience_level = models.CharField(max_length=20, blank=True, null=True)
    resume_url = models.TextField(blank=True, null=True)
    skills = ArrayField(models.CharField(max_length=100), default=list, blank=True)

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)