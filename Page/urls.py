from django.urls import path
from .views import page_list, create_page, update_page, delete_page
from . import views

urlpatterns = [
    path('', page_list, name='page_list'),
    path('<int:chapter_id>/page/<int:page_id>/', views.page_detail, name='page_detail'),
    path('create/', create_page, name='create_page'),
    path('update/<int:pk>/', update_page, name='update_page'),
    path('delete/<int:pk>/', delete_page, name='delete_page'),
]
