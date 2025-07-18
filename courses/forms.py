from django import forms
from .models import Course, Category, Tag, Lesson, Assignment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'tags', 'price',]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'tags': forms.CheckboxSelectMultiple(),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional, useful if you want to limit categories dynamically
        self.fields['category'].queryset = Category.objects.all()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter tag name'}),
        }
    
    def uniqe_tag(self):
        name = self.cleaned_data.get('name')
        if Tag.objects.filter(name=name).exists():
            raise forms.ValidationError("Tag already exists.")
        return name
    
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'description', 'video_url', 'resource', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'video_url': forms.URLInput(attrs={'placeholder': 'Enter video URL'}),
            'resource': forms.ClearableFileInput(),
            'order': forms.NumberInput(attrs={'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # limit courses dynamically
        self.fields['course'].queryset = Course.objects.all()

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['lesson', 'title', 'description', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # limit courses dynamically
        self.fields['course'].queryset = Course.objects.all()