from django.shortcuts import render, redirect
from .models import Instructor
from users.forms import UserForm
from .forms import InstructorForm

def instructor_profile(request):
    if request.method == 'POST':
        instructor_form = InstructorForm(request.POST, request.FILES or None)
        user_form = UserForm(request.POST, request.FILES or None)

        if instructor_form.is_valid() and user_form.is_valid():
            # Create user and instructor
            user = user_form.save(commit=False)
            user.role = 'instructor'
            user.save()  # Save user first to get user.id
            instructor = instructor_form.save(commit=False) 
            instructor.user = user
            instructor.save()
            return redirect('instructor_list')
    else:
        instructor_form = InstructorForm()
        user_form = UserForm(initial={'role': 'instructor'})  # Set initial role to instructor
    return render(request, 'instructors/add_instructor.html', {'instructor_form': instructor_form, 'user_form': user_form})

def instructor_list(request):
    instructors = Instructor.objects.select_related('user').all()
    return render(request, 'instructors/instructor_list.html', {'instructors': instructors})

def instructor_edit(request,pk):
    instructor = Instructor.objects.filter(pk=pk).first()
    user = instructor.user
    instructor_form = InstructorForm(request.POST or None, instance=instructor)
    user_form = UserForm(request.POST or None, instance=user)
    
    if 'role' in user_form.fields:
        user_form.fields.pop('role')  # Remove role field to prevent editing role
    
    if instructor_form.is_valid() and user_form.is_valid():
        instructor = instructor_form.save(commit=False)
        user = user_form.save()
        instructor.user = user
        instructor.save()
        return redirect('instructor_list')
    
    return render(request, 'instructors/edit_instructor.html', {'instructor_form': instructor_form, 'user_form': user_form})

def instrucrtor_delete(request, pk):
    instructor = Instructor.objects.filter(pk=pk).first()
    if request.method == 'POST':
        instructor.delete()
        return redirect('instructor_list')
    return render(request, 'instructors/delete_instructor.html', {'instructor': instructor})

