from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CourseForm,SubmissionForm,CategoryForm,TagForm,LessonForm,AssignmentForm
from .models import Course,Tag,Instructor,Category,Assignment, Submission,Lesson
from enrollments.models import Enrollment

@login_required
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
@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.instructor
            course.created_by = request.user 
            course.save()
            form.save_m2m()  
            return redirect('course_list') 
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form, 'title': 'Create Course'})  
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user.instructor)
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('instructor_course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'title': 'Edit Course'})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user.instructor)
    if request.method == 'POST':
        course.delete()
        return redirect('instructor_course_list')
    return render(request, 'courses/delete_course.html', {'course': course})

@login_required
def student_course_list(request):
    if hasattr(request.user, 'student'):
        student = request.user.student
        enrollments = Enrollment.objects.filter(student=student).select_related('course')
        enrolled_courses = [enrollment.course for enrollment in enrollments]
        context = {
            'enrollments': enrollments,
            'enrolled_courses': enrolled_courses,
        }
        return render(request, 'courses/student_course_list.html', context)
    else:
        return redirect('/')
@login_required
def instrctor_course_list(request):
    if hasattr(request.user, 'instructor'):
        instructor = request.user.instructor
        myCourses = Course.objects.filter(instructor=instructor)
        context = {
            'myCourses': myCourses,
        }
        return render(request, 'courses/instructor_course_list.html', context)
    else:
        return redirect('/')

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'courses/category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'courses/add_category.html', {'form': form, 'title': 'Add Category'})


@login_required
def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category_form = CategoryForm(request.POST or None, instance=category)
    if category_form.is_valid():    
        category_form.save()
        return redirect('category_list')
    return render(request, 'courses/edit_category.html', {'category_form': category_form, 'title': 'Edit Category'})
@login_required
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'courses/delete_category.html', {'category': category})
@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'courses/tag_list.html', {'tags': tags})

@login_required
def add_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Tag.objects.create(name=name)
            return redirect('tag_list')
    return render(request, 'courses/add_tag.html')

def assignment_list(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    assignments = lesson.assignments.all()
    return render(request, 'courses/assignment_list.html', {'lesson': lesson, 'assignments': assignments})

def assignment_detail(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    submissions = assignment.submissions.all()
    return render(request, 'courses/assignment_detail.html', {'assignment': assignment, 'submissions': submissions})

def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    student = request.user.student 

    submission, created = Submission.objects.get_or_create(
        assignment=assignment,
        student=student
    )
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')  # Redirect to a student dashboard or assignment detail page
    else:
        form = SubmissionForm(instance=submission)
    return render(request, 'courses/submit_assignment.html', {'form': form, 'assignment': assignment})

def create_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user.instructor)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm()
    return render(request, 'courses/create_lesson.html', {'form': form, 'course': course})
