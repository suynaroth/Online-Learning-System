from django.contrib import admin
from django.urls import path,include
from students import urls as student_url
from instructors import urls as instructor_url
from courses import urls as course_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path("students/",include(student_url)),
    path("instructors/",include(instructor_url)),
    path("courses/",include(course_url)),
]
