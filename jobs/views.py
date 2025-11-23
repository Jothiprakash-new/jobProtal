from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Job, Application, Interview
from .serializers import JobSerializer, JobCreateSerializer, ApplicationSerializer, ApplicationCreateSerializer, InterviewSerializer
from accounts.models import EmployerProfile, JobSeekerProfile

@api_view(['GET', 'POST'])
def jobs(request):
    if request.method == 'GET':
        queryset = Job.objects.filter(is_active=True)
        # Filtering
        location = request.query_params.get('location')
        job_type = request.query_params.get('job_type')
        experience_level = request.query_params.get('experience_level')
        skills = request.query_params.get('skills')  # comma separated

        if location:
            queryset = queryset.filter(location__icontains=location)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
        if skills:
            skill_list = skills.split(',')
            for skill in skill_list:
                queryset = queryset.filter(skills_required__icontains=skill.strip())

        serializer = JobSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Only employers can post jobs
        try:
            employer = EmployerProfile.objects.get(user=request.user)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Only employers can post jobs'}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posted_by=request.user, company=employer.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def job_detail(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)
    elif request.method in ['PUT', 'DELETE']:
        # Only the poster can edit/delete
        if job.posted_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'PUT':
            serializer = JobCreateSerializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            job.is_active = False
            job.save()
            return Response({'message': 'Job deactivated'})

@api_view(['GET', 'POST'])
def applications(request):
    if request.method == 'GET':
        # Job seekers see their applications, employers see applications for their jobs
        if request.user.role == 'job_seeker':
            try:
                seeker = JobSeekerProfile.objects.get(user=request.user)
                applications = Application.objects.filter(seeker=seeker)
            except JobSeekerProfile.DoesNotExist:
                return Response([])
        elif request.user.role == 'employer':
            try:
                employer = EmployerProfile.objects.get(user=request.user)
                applications = Application.objects.filter(job__company=employer.company)
            except EmployerProfile.DoesNotExist:
                return Response([])
        else:
            return Response({'error': 'Invalid role'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Only job seekers can apply
        try:
            seeker = JobSeekerProfile.objects.get(user=request.user)
        except JobSeekerProfile.DoesNotExist:
            return Response({'error': 'Job seeker profile required'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ApplicationCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Check if already applied
            if Application.objects.filter(job=serializer.validated_data['job'], seeker=seeker).exists():
                return Response({'error': 'Already applied'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(seeker=seeker)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_application_status(request, pk):
    try:
        application = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

    # Only employer of the job can update
    try:
        employer = EmployerProfile.objects.get(user=request.user, company=application.job.company)
    except EmployerProfile.DoesNotExist:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    new_status = request.data.get('status')
    if new_status in dict(Application.STATUS_CHOICES):
        application.status = new_status
        application.save()
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)
    return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def interviews(request):
    if request.method == 'GET':
        # Similar to applications
        if request.user.role == 'job_seeker':
            try:
                seeker = JobSeekerProfile.objects.get(user=request.user)
                interviews = Interview.objects.filter(application__seeker=seeker)
            except JobSeekerProfile.DoesNotExist:
                return Response([])
        elif request.user.role == 'employer':
            try:
                employer = EmployerProfile.objects.get(user=request.user)
                interviews = Interview.objects.filter(application__job__company=employer.company)
            except EmployerProfile.DoesNotExist:
                return Response([])
        else:
            return Response({'error': 'Invalid role'}, status=status.HTTP_403_FORBIDDEN)

        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Only employers can schedule interviews
        try:
            employer = EmployerProfile.objects.get(user=request.user)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Only employers can schedule interviews'}, status=status.HTTP_403_FORBIDDEN)

        serializer = InterviewSerializer(data=request.data)
        if serializer.is_valid():
            # Check if application belongs to employer's company
            if serializer.validated_data['application'].job.company != employer.company:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(interviewer=employer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
