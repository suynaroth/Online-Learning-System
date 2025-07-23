from django.shortcuts import render,redirect
from .models import Student
from users.models import User
from .forms import StudentForm
from users.forms import UserForm

def student_list(request):
    students = Student.objects.select_related('user').all()
    return render(request,'students/student_list.html', {'students' : students})

def student_registration(request):
    if request.method == 'POST':
        # For POST requests, instantiate forms with submitted data
        student_form = StudentForm(request.POST, request.FILES or None)
        user_form = UserForm(request.POST, request.FILES or None) 
        
        if student_form.is_valid() and user_form.is_valid():
            # Create user and student
            user = user_form.save(commit=False)
            user.role = 'student'
            user.save()
            student = student_form.save(commit=False) #save in memory for temp
            student.user = user      # Link student to the saved user
            student.save()
            return redirect('student_list')
    else: # This block handles GET requests
        # For GET requests, instantiate empty forms
        student_form = StudentForm()
        user_form = UserForm()  # Set initial role for the user form
    #will be executed for initial GET requests and also if POST forms are invalid (after the 'else' in the POST block)
    return render(request, 'students/student_form.html', {'student_form': student_form,'user_form': user_form})

def edit_student(request, pk):
    student = Student.objects.filter(pk=pk).first()
    user = student.user
    student_form = StudentForm(request.POST or None,instance=student)
    user_form = UserForm(request.POST or None, instance=user)
    if 'role' in user_form.fields:
        user_form.fields.pop('role')  # Remove role field to prevent editing role
    if student_form.is_valid() and user_form.is_valid():
        student = student_form.save(commit=False)
        user = user_form.save()
        student.user = user
        student.save()
        return redirect('student_list')
    return render(request, 'students/edit_student.html', {'student_form': student_form,'user_form': user_form})

def delete_student(request, pk):
    student = Student.objects.filter(pk=pk).first()
    if request.method == 'POST':
        student.user.delete()
        # student.delete()
        return redirect('student_list')
    return render(request, 'students/delete_student.html', {'student': student})  