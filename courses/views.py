from django.shortcuts import render,redirect
from .forms import CourseForm
from .models import Course

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

def course_list(request):
    courses = Course.objects.all()

    #for filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        courses = courses.filter(category__name=category_filter)

    #for filter by tag
    tag_filter = request.GET.get('tag')
    if tag_filter:
        courses = courses.filter(tags__name=tag_filter) 
        
    return render(request, 'courses/courses_list.html', {'courses': courses})