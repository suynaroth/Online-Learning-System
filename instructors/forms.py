from django import forms
from .models import Instructor

class InstructorForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'date_of_birth','expertise']