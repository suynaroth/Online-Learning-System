from django import forms
from .models import Student
from users.models import User

class StudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={' type': ' date'}))
    class Meta:
        model = Student
        fields = ['first_name', 'last_name','phone_number', 'address', 'date_of_birth']
        