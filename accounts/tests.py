from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, JobSeekerProfile, EmployerProfile, Company

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='test@example.com', email='test@example.com', password='pass', role='job_seeker')
        self.assertEqual(user.username, 'test@example.com')
        self.assertEqual(user.role, 'job_seeker')

class JobSeekerProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seeker@example.com', email='seeker@example.com', password='pass', role='job_seeker')

    def test_profile_creation(self):
        profile = JobSeekerProfile.objects.create(user=self.user, experience_level='fresher')
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.experience_level, 'fresher')

class EmployerProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employer@example.com', email='employer@example.com', password='pass', role='employer')
        self.company = Company.objects.create(name='Test Company')

    def test_profile_creation(self):
        profile = EmployerProfile.objects.create(user=self.user, company=self.company, position='Manager')
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.company, self.company)

class CompanyModelTest(TestCase):
    def test_company_creation(self):
        company = Company.objects.create(name='Test Company', industry='Tech', size='50-100')
        self.assertEqual(company.name, 'Test Company')
        self.assertEqual(company.industry, 'Tech')

class RegisterViewTest(APITestCase):
    def test_register_job_seeker(self):
        data = {
            'email': 'seeker@example.com',
            'password': 'pass',
            'role': 'job_seeker',
            'experience': 'fresher'
        }
        response = self.client.post('/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='seeker@example.com').exists())
        self.assertTrue(JobSeekerProfile.objects.filter(user__email='seeker@example.com').exists())

    def test_register_employer(self):
        data = {
            'email': 'employer@example.com',
            'password': 'pass',
            'role': 'employer',
            'company': 'Test Company',
            'position': 'Manager'
        }
        response = self.client.post('/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='employer@example.com').exists())
        self.assertTrue(EmployerProfile.objects.filter(user__email='employer@example.com').exists())
        self.assertTrue(Company.objects.filter(name='Test Company').exists())

class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@example.com', email='test@example.com', password='pass', role='job_seeker')

    def test_login_success(self):
        data = {'email': 'test@example.com', 'password': 'pass'}
        response = self.client.post('/accounts/login/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['msg'], 'Login successful')

    def test_login_failure(self):
        data = {'email': 'test@example.com', 'password': 'wrong'}
        response = self.client.post('/accounts/login/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['msg'], 'Invalid credentials')