from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('home')
    return render(request, 'dashboards/student_dashboard.html')

@login_required
def instructor_dashboard(request):
    if request.user.role != 'instructor':
        return redirect('home')
    return render(request, 'dashboards/instructor_dashboard.html')

@login_required
def employee_dashboard(request):
    if request.user.role != 'employee':
        return redirect('home')
    return render(request, 'dashboards/employee_dashboard.html')

