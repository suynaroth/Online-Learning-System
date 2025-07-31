from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from courses.models import Course, Assignment
from enrollments.models import Enrollment

@login_required
def student_dashboard(request):
    if hasattr (request.user, 'student'):

        student = request.user.student
        enrollments = Enrollment.objects.filter(student=student).select_related('course')

        enrolled_courses = [enrollment.course for enrollment in enrollments]

        homework = Assignment.objects.filter(lesson__course__in=enrolled_courses)

        other_courses = Course.objects.exclude(id__in=[c.id for c in enrolled_courses])

        context = {
            'enrollments': enrollments,
            'enrolled_courses': enrolled_courses,
            'homework': homework,
            'other_courses': other_courses,
        }
        
        return render(request, 'dashboards/student_dashboard.html', context)
    else:
        return redirect('/')
        
@login_required
def instructor_dashboard(request):
    if hasattr(request.user, 'instructor'):
        instructor = request.user.instructor
        courses = Course.objects.filter(instructor=instructor).select_related('course')


        context = {
            'courses': courses,
        }
        
        return render(request, 'dashboards/instructor_dashboard.html', context)
    else:
        return redirect('/')

