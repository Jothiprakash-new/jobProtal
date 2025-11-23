from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, JobSeekerProfile, EmployerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = JobSeekerProfile
        fields = '__all__'

class EmployerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanySerializer()

    class Meta:
        model = EmployerProfile
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user