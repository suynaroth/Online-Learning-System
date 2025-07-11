from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('registration/', views.student_registration, name='student_registration'),
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
]