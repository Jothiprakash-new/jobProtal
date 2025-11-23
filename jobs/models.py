from django.db import models
from accounts.models import User, Company, JobSeekerProfile, EmployerProfile

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    location_type = models.CharField(max_length=50, choices=[('remote', 'Remote'), ('onsite', 'Onsite'), ('hybrid', 'Hybrid')])
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    experience_required = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50, choices=[('full-time', 'Full-time'), ('part-time', 'Part-time'), ('internship', 'Internship')])
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField(null=True, blank=True)
    skills_required = models.TextField(blank=True)

class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateTimeField(auto_now_add=True)

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    feedback = models.TextField(blank=True)
