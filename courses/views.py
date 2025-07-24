from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import CourseForm,SubmissionForm,CategoryForm,TagForm,LessonForm,AssignmentForm
from .models import Course,Tag,Instructor,Category,Assignment, Submission,Lesson

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
def student_course_list(request):
    if hasattr(request.user, 'student'):
        student = request.user.student
        all_courses = Course.objects.all()
        enrolled_ids = student.enrolled_courses.values_list('id', flat=True)

        return render(request, 'courses/student_course_list.html', {
            'all_courses': all_courses,
            'enrolled_ids': enrolled_ids,
        })
    else:
        return redirect('/')


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



def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category_form = CategoryForm(request.POST or None, instance=category)
    if category_form.is_valid():    
        category_form.save()
        return redirect('category_list')
    return render(request, 'courses/edit_category.html', {'category_form': category_form, 'title': 'Edit Category'})

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'courses/delete_category.html', {'category': category})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'courses/tag_list.html', {'tags': tags})

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