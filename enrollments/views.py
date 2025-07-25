from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from courses.models import Course
from .models import Enrollment

@login_required
def enroll(request, course_id):
    course = Course.objects.get(id=course_id)
    student = request.user.student
    enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
    if created:
        messages.success(request, f"You have successfully enrolled in {course.title}.")
    else:
        messages.info(request, f"You are already enrolled in {course.title}.")
    return redirect('student_course_list')

