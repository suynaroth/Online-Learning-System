from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('', views.instructor_dashboard, name='instructor_dashboard'),
]
