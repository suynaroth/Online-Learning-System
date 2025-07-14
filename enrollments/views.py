from django.shortcuts import render,redirect
from courses.models import Course
from .models import Enrollment

def enroll(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(student=request.user.student, course=course)
        if created:
            return redirect('enrollment_success', course_id=course.id)
        else:
            return redirect('already_enrolled', course_id=course.id)
    return render(request, 'enrollments/enroll.html', {'course': course})
