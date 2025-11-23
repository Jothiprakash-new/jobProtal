from rest_framework import serializers
from .models import Job, Application, Interview
from accounts.models import JobSeekerProfile, EmployerProfile, Company
from accounts.serializers import CompanySerializer

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    seeker = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class InterviewSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'