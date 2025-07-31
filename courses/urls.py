from django.urls import path
from .views import (create_course, course_list,instrctor_course_list,edit_course,delete_course,submit_assignment,category_list, 
                    add_category,edit_category,delete_category,create_lesson,
                     student_course_list, tag_list, add_tag, assignment_list, assignment_detail)

urlpatterns = [
    path('', course_list, name='course_list'),
    path('edit/<int:course_id>/', edit_course, name='edit_course'),
    path('delete/<int:course_id>/', delete_course, name='delete_course'),
    path('student/', student_course_list, name='student_course_list'),
    path('instructor/', instrctor_course_list, name='instructor_course_list'),
    path('create/', create_course, name='create_course'),
    path('submit_assignment/<int:assignment_id>/', submit_assignment, name='submit_assignment'),
    path('categories/', category_list, name='category_list'),
    path('categories/add/', add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    path('lessons/create/<int:course_id>/', create_lesson, name='create_lesson'),

]