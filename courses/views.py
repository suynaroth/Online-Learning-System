from django.shortcuts import render,redirect
from .forms import CourseForm

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user  # Assuming the user is logged in
            course.instructor = request.user.instructor
            course.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('course_list')  # Redirect to a course list or detail view
    else:
        form = CourseForm()
    
    return render(request, 'courses/create_course.html', {'form': form})
