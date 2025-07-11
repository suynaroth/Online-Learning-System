from django.shortcuts import render,redirect
from .models import Student
from users.models import User
from .forms import StudentForm

def student_list(request):
    students = Student.objects.select_related('user').all()
    return render(request,'students/student_list.html', {'students' : students})

def student_registration(request):
    if request.method == 'POST':
        form = StudentForm(request.POST or None)
        username = request.POST.get('username')
        password = request.POST.get()
        
        if form.is_valid() and username and password:
            #create user
            user = User.objects.create_user(
                username=username,
                password=password,
                role = 'student'
            )

            #creat student and link to user
            student = form.save(commit=False) #use commit = false to not record the data to database just save in memeory
            student.user = user
            student.save()
            return redirect('student_list')
        return render(request,'students/student_form.html' , {'form' : form})

def edit_student(request, pk):
    student = Student.objects.filter(pk=pk).first()
    form = StudentForm(request.POST or None,instance=student)
    if form.is_valid():
        form.save

    
