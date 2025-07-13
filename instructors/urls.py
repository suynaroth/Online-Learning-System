from django.urls import path
from . import views

urlpatterns = [
    path('', views.instructor_list, name='instructor_list'),
    path('registration/', views.instructor_profile, name='instructor_profile'),
    path('edit/<int:pk>/', views.instructor_edit, name='instructor_edit'),
    path('delete/<int:pk>/', views.instrucrtor_delete, name='instructor_delete'),
]