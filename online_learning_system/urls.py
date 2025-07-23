from django.contrib import admin
from django.urls import path,include
from students import urls as student_url
from instructors import urls as instructor_url
from courses import urls as course_url
from django.contrib.auth import views as auth_views
from dashboards.forms import LoginForm

urlpatterns = [
    path('', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('admin/', admin.site.urls),
    path("students/",include('students.urls')),
    path("instructors/",include(instructor_url)),
    path("courses/",include(course_url)),
    path('dashboards/', include('dashboards.urls')),
    path('enrollments/', include('enrollments.urls')),
]
