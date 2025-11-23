from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('applications/', views.applications, name='applications'),
    path('applications/<int:pk>/status/', views.update_application_status, name='update_application_status'),
    path('interviews/', views.interviews, name='interviews'),
]