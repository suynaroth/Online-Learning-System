from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from courses.models import Course, Assignment

@login_required
def student_dashboard(request):
    if hasattr (request.user, 'student'):

        student = request.user.student
        enrolled_courses = student.enrolled_courses.all()

        homework = Assignment.objects.filter(lesson__course__in=enrolled_courses)

        all_courses = Course.objects.exclude(id__in=enrolled_courses.values_list('id', flat=True))

        context = {
            'enrolled_courses': enrolled_courses,
            'homework': homework,
            'other_courses': all_courses,
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

