from django.contrib import admin
from django.urls import path,include
from students import urls as student_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path("students/",include(student_url)),
]
