from django.shortcuts import render,redirect
from .forms import CourseForm
from .models import Course,Tag,Instructor,Category

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
    tags = Tag.objects.all()
    categories = Category.objects.all()
    instructors = Instructor.objects.all()

    #for filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        courses = courses.filter(category_id = category_filter)

    #for filter by tag
    tag_filter = request.GET.get('tag')
    if tag_filter:
        courses = courses.filter(tags_id = tag_filter) 

    #filter by instructor
    instructor_filter = request.GET.get('instructor')
    if instructor_filter:
        courses = courses.filter(instructors_id = instructor_filter)
        
    return render(request, 'courses/courses_list.html', {'courses': courses,
                                                         'tags': tags,
                                                         'categories': categories,
                                                         'instructors': instructors
                                                         })