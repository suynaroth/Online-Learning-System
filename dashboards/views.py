from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from courses.models import Course, Assignment
from enrollments.models import Enrollment
from instructors.models import Instructor
from students.models import Student 
from employees.models import Employee

@login_required
def dashboard(request):
    if hasattr (request.user, 'student'):

        student = Student.objects.get(user=request.user)
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
    elif hasattr(request.user, 'instructor'):
        instructor = Instructor.objects.get(user=request.user)
        courses = Course.objects.filter(instructor=instructor)

        context = {
            'courses': courses,
        }
        
        return render(request, 'dashboards/instructor_dashboard.html', context)
    elif hasattr(request.user, 'employee'):
        employee = Employee.objects.get(user=request.user)
        context = {
            'employee': employee,
        }
        
        return render(request, 'dashboards/employee_dashboard.html', context)
    else:
        return redirect('home')
    