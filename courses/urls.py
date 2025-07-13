from django.urls import path
from .views import create_course, course_list

urlpatterns = [
    path('', course_list, name='course_list'),
    path('create/', create_course, name='create_course'),
]