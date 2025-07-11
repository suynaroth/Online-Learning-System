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
            user = user_form.save()
            student = student_form.save(commit=False) #save in memory for temp
            student.user = user      # Link student to the saved user
            student.save()
            return redirect('student_list')
    else: # This block handles GET requests
        # For GET requests, instantiate empty forms
        student_form = StudentForm()
        user_form = UserForm()
       
    #will be executed for initial GET requests and also if POST forms are invalid (after the 'else' in the POST block)
    return render(request, 'students/student_form.html', {'student_form': student_form,'user_form': user_form})

def edit_student(request, pk):
    student = Student.objects.filter(pk=pk).first()
    form = StudentForm(request.POST or None,instance=student)
    if form.is_valid():
        form.save

    
