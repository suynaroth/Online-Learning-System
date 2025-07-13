from django import forms
from .models import Course, Category

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'tags', 'price', 'image', 'published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'tags': forms.CheckboxSelectMultiple(),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional, useful if you want to limit categories dynamically
        self.fields['category'].queryset = Category.objects.all()
