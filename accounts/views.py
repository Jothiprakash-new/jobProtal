from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User, JobSeekerProfile, EmployerProfile
from django.contrib.auth import authenticate

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
            role=data["role"]
        )
        if user.role == "job_seeker":
            JobSeekerProfile.objects.create(user=user, experience_level=data["experience"])
        else:
            company, created = Company.objects.get_or_create(name=data["company"])
            EmployerProfile.objects.create(user=user, company=company, position=data.get("position", ""))

        return Response({"msg": "User registered"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data["email"], password=request.data["password"])
        if user:
            return Response({"msg": "Login successful"})
        return Response({"msg": "Invalid credentials"}, status=400)
