# exercices/urls.py
from django.urls import path
from . import views

urlpatterns = [
   path('', views.ExerciceListView.as_view(), name='exercice_list'),
    path('<int:pk>/', views.ExerciceDetailView.as_view(), name='exercice_detail'),
    path('create/', views.ExerciceCreateView.as_view(), name='exercice_create'),
    path('<int:pk>/update/', views.ExerciceUpdateView.as_view(), name='exercice_update'),
    path('<int:pk>/delete/', views.ExerciceDeleteView.as_view(), name='exercice_confirm_delete'),
    
    #path('reponses/', views.ReponseExerciceListView.as_view(), name='reponse_list'),
    #path('reponses/new/', views.ReponseExerciceCreateView.as_view(), name='reponse_create'),
    #path('reponses/<int:pk>/', views.ReponseExerciceDetailView.as_view(), name='reponse_detail'),
    #path('reponses/<int:pk>/update/', views.ReponseExerciceUpdateView.as_view(), name='reponse_update'),
    #path('reponses/<int:pk>/delete/', views.ReponseExerciceDeleteView.as_view(), name='reponse_delete'),
]
