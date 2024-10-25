from django.urls import path
from .views import chapter_list, create_chapter, update_chapter, delete_chapter
from . import views

urlpatterns = [
    path('', chapter_list, name='chapter_list'),
    path('<int:course_id>/', views.chapter_list, name='course_chapter_list'),
    path('create/<int:course_id>/', create_chapter, name='create_chapter'),
    path('update/<int:pk>/', update_chapter, name='update_chapter'),
    path('delete/<int:pk>/', delete_chapter, name='delete_chapter'),
]
