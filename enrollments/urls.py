from django.urls import path
from .views import enroll

urlpatterns = [
    path('enroll/<int:course_id>/', enroll, name='enroll'),

]