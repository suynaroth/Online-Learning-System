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
        

# @login_required
# def instructor_dashboard(request):
#     if request.user.role != 'instructor':
#         # return redirect('home')
#     return render(request, 'dashboards/instructor_dashboard.html')

# # @login_required
# def employee_dashboard(request):
#     if request.user.role != 'employee':
#         # return redirect('home')
#     return render(request, 'dashboards/employee_dashboard.html')

