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
        student_form = StudentForm(request.POST or None)
        user_form = UserForm(request.POST or None)
        
        if student_form.is_valid() and user_form.is_valid():
            #create user and student
            student = student_form.save(commit=False)  #not record the data to database just save in memeory for temp
            user = user_form.save()

            #link student to user
            student.user = user
            student.save()
            return redirect('student_list')
        return render(request,'students/student_form.html' , {'student_form' : student_form, 'user_form': user_form})

def edit_student(request, pk):
    student = Student.objects.filter(pk=pk).first()
    form = StudentForm(request.POST or None,instance=student)
    if form.is_valid():
        form.save

    
