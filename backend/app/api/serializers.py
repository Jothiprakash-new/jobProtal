from rest_framework import serializers
from core.models import User, Company, JobSeeker, Job, Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','role','profile_status']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'