from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ('job_seeker', 'Job Seeker'),
    ('employer', 'Employer'),
)

EXPERIENCE_CHOICES = (
    ('fresher', 'Fresher'),
    ('experienced', 'Experienced'),
)

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    profile_completed = models.BooleanField(default=False)


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    projects = models.TextField(null=True, blank=True)
    certifications = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=50, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)

    def __str__(self):
        return self.company.name
