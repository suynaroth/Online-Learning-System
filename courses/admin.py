from django.contrib import admin
from .models import Course, Category, Tag, Lesson, Assignment

admin.site.register(Course)
admin.site.register(Category)   
admin.site.register(Tag)    
admin.site.register(Lesson)
admin.site.register(Assignment)
