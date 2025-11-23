from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from .models import Job, Application, Interview
from accounts.models import User, JobSeekerProfile, EmployerProfile, Company

class JobModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.company = Company.objects.create(name='Test Company')
        self.employer = EmployerProfile.objects.create(user=self.user, company=self.company, position='Manager')

    def test_job_creation(self):
        job = Job.objects.create(
            company=self.company,
            title='Developer',
            description='Job desc',
            requirements='Req',
            location='NY',
            location_type='remote',
            experience_required='2 years',
            job_type='full-time',
            posted_by=self.user,
            skills_required='Python'
        )
        self.assertEqual(job.title, 'Developer')
        self.assertEqual(job.company, self.company)

class ApplicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seeker@example.com', email='seeker@example.com', password='pass', role='job_seeker')
        self.seeker = JobSeekerProfile.objects.create(user=self.user, experience_level='fresher')
        self.company = Company.objects.create(name='Test Company')
        self.employer_user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.employer = EmployerProfile.objects.create(user=self.employer_user, company=self.company, position='Manager')
        self.job = Job.objects.create(
            company=self.company,
            title='Developer',
            description='Job desc',
            requirements='Req',
            location='NY',
            location_type='remote',
            experience_required='2 years',
            job_type='full-time',
            posted_by=self.employer_user,
            skills_required='Python'
        )

    def test_application_creation(self):
        application = Application.objects.create(job=self.job, seeker=self.seeker)
        self.assertEqual(application.job, self.job)
        self.assertEqual(application.seeker, self.seeker)
        self.assertEqual(application.status, 'applied')

class InterviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seeker@example.com', email='seeker@example.com', password='pass', role='job_seeker')
        self.seeker = JobSeekerProfile.objects.create(user=self.user, experience_level='fresher')
        self.company = Company.objects.create(name='Test Company')
        self.employer_user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.employer = EmployerProfile.objects.create(user=self.employer_user, company=self.company, position='Manager')
        self.job = Job.objects.create(
            company=self.company,
            title='Developer',
            description='Job desc',
            requirements='Req',
            location='NY',
            location_type='remote',
            experience_required='2 years',
            job_type='full-time',
            posted_by=self.employer_user,
            skills_required='Python'
        )
        self.application = Application.objects.create(job=self.job, seeker=self.seeker)

    def test_interview_creation(self):
        interview = Interview.objects.create(application=self.application, interviewer=self.employer, schedule=timezone.now())
        self.assertEqual(interview.application, self.application)
        self.assertEqual(interview.interviewer, self.employer)

class JobsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.company = Company.objects.create(name='Test Company')
        self.employer = EmployerProfile.objects.create(user=self.user, company=self.company, position='Manager')
        self.client.force_authenticate(user=self.user)

    def test_get_jobs(self):
        Job.objects.create(
            company=self.company,
            title='Developer',
            description='Job desc',
            requirements='Req',
            location='NY',
            location_type='remote',
            experience_required='2 years',
            job_type='full-time',
            posted_by=self.user,
            skills_required='Python'
        )
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_job(self):
        data = {
            'title': 'Developer',
            'description': 'Job desc',
            'requirements': 'Req',
            'location': 'NY',
            'location_type': 'remote',
            'experience_required': '2 years',
            'job_type': 'full-time',
            'skills_required': 'Python'
        }
        response = self.client.post('/jobs/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Job.objects.filter(title='Developer').exists())

    def test_post_job_unauthorized(self):
        seeker_user = User.objects.create_user(username='seeker@example.com', email='seeker@example.com', password='pass', role='job_seeker')
        self.client.force_authenticate(user=seeker_user)
        data = {
            'title': 'Developer',
            'description': 'Job desc',
            'requirements': 'Req',
            'location': 'NY',
            'location_type': 'remote',
            'experience_required': '2 years',
            'job_type': 'full-time',
            'skills_required': 'Python'
        }
        response = self.client.post('/jobs/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class JobDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.company = Company.objects.create(name='Test Company')
        self.employer = EmployerProfile.objects.create(user=self.user, company=self.company, position='Manager')
        self.job = Job.objects.create(
            company=self.company,
            title='Developer',
            description='Job desc',
            requirements='Req',
            location='NY',
            location_type='remote',
            experience_required='2 years',
            job_type='full-time',
            posted_by=self.user,
            skills_required='Python'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_job_detail(self):
        response = self.client.get(f'/jobs/{self.job.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Developer')

    def test_put_job_detail(self):
        data = {'title': 'Senior Developer'}
        response = self.client.put(f'/jobs/{self.job.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, 'Senior Developer')

    def test_delete_job_detail(self):
        response = self.client.delete(f'/jobs/{self.job.id}/')
        self.assertEqual(response.status_code, 200)
        self.job.refresh_from_db()
        self.assertFalse(self.job.is_active)

class ApplicationsViewTest(APITestCase):
    def setUp(self):
        self.seeker_user = User.objects.create_user(username='seeker@example.com', email='seeker@example.com', password='pass', role='job_seeker')
        self.seeker = JobSeekerProfile.objects.create(user=self.seeker_user, experience_level='fresher')
        self.company = Company.objects.create(name='Test Company')
        self.employer_user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.employer = EmployerProfile.objects.create(user=self.employer_user, company=self.company, position='Manager')
        self.job = Job.objects.create(
            company=self.company,
            title='Developer',
            description='Job desc',
            requirements='Req',
            location='NY',
            location_type='remote',
            experience_required='2 years',
            job_type='full-time',
            posted_by=self.employer_user,
            skills_required='Python'
        )

    def test_get_applications_seeker(self):
        self.client.force_authenticate(user=self.seeker_user)
        Application.objects.create(job=self.job, seeker=self.seeker)
        response = self.client.get('/jobs/applications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_application(self):
        self.client.force_authenticate(user=self.seeker_user)
        data = {'job': self.job.id}
        response = self.client.post('/jobs/applications/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Application.objects.filter(job=self.job, seeker=self.seeker).exists())

class UpdateApplicationStatusViewTest(APITestCase):
    def setUp(self):
        self.seeker_user = User.objects.create_user(username='seeker@example.com', email='seeker@example.com', password='pass', role='job_seeker')
        self.seeker = JobSeekerProfile.objects.create(user=self.seeker_user, experience_level='fresher')
        self.company = Company.objects.create(name='Test Company')
        self.employer_user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.employer = EmployerProfile.objects.create(user=self.employer_user, company=self.company, position='Manager')
        self.job = Job.objects.create(
            company=self.company,
            title='Developer',
            description='Job desc',
            requirements='Req',
            location='NY',
            location_type='remote',
            experience_required='2 years',
            job_type='full-time',
            posted_by=self.employer_user,
            skills_required='Python'
        )
        self.application = Application.objects.create(job=self.job, seeker=self.seeker)
        self.client.force_authenticate(user=self.employer_user)

    def test_update_status(self):
        data = {'status': 'shortlisted'}
        response = self.client.put(f'/jobs/applications/{self.application.id}/status/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'shortlisted')

class InterviewsViewTest(APITestCase):
    def setUp(self):
        self.seeker_user = User.objects.create_user(username='seeker@example.com', email='seeker@example.com', password='pass', role='job_seeker')
        self.seeker = JobSeekerProfile.objects.create(user=self.seeker_user, experience_level='fresher')
        self.company = Company.objects.create(name='Test Company')
        self.employer_user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.employer = EmployerProfile.objects.create(user=self.employer_user, company=self.company, position='Manager')
        self.job = Job.objects.create(
            company=self.company,
            title='Developer',
            description='Job desc',
            requirements='Req',
            location='NY',
            location_type='remote',
            experience_required='2 years',
            job_type='full-time',
            posted_by=self.employer_user,
            skills_required='Python'
        )
        self.application = Application.objects.create(job=self.job, seeker=self.seeker)

    def test_get_interviews_employer(self):
        self.client.force_authenticate(user=self.employer_user)
        Interview.objects.create(application=self.application, interviewer=self.employer, schedule=timezone.now())
        response = self.client.get('/jobs/interviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_interview(self):
        self.client.force_authenticate(user=self.employer_user)
        data = {'application': self.application.id, 'schedule': timezone.now().isoformat()}
        response = self.client.post('/jobs/interviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Interview.objects.filter(application=self.application).exists())