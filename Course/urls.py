from django.urls import path
from .views import course_list, create_course, update_course, delete_course

urlpatterns = [
    path('', course_list, name='course_list'),
    path('create/', create_course, name='create_course'),
    path('update/<int:pk>/', update_course, name='update_course'),
    path('delete/<int:pk>/', delete_course, name='delete_course'),
]
