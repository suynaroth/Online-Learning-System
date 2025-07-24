from django.urls import path
from .views import (create_course, course_list,submit_assignment,category_list, 
                    add_category,edit_category,delete_category, tag_list, add_tag, assignment_list, assignment_detail)

urlpatterns = [
    path('', course_list, name='course_list'),
    path('create/', create_course, name='create_course'),
    path('submit_assignment/<int:assignment_id>/', submit_assignment, name='submit_assignment'),
    path('categories/', category_list, name='category_list'),
    path('categories/add/', add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
]