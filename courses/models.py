from django.db import models
from django.conf import settings
from users.models import User
from instructors.models import Instructor

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    tags = models.ManyToManyField(Tag, blank=True, related_name='courses')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)  # URL to the lesson video
    resource = models.FileField(upload_to='resources/', blank=True, null=True)  # Optional resource file
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order') #lessons in a course have unique order numbers

class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['due_date']     

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'Submission by {self.student.username} for {self.assignment.title}'
    
    class Meta:
        unique_together = ('assignment', 'student')  # A student can submit only once per assignment
        ordering = ['-submitted_at']  # Most recent submissions first                                                              