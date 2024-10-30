# exercices/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.ExerciceListUserView.as_view(), name='exercice_list_user'),  # User list view with "passer" button
    path('', views.ExerciceListView.as_view(), name='exercice_list'),  # Admin list view
    path('user/<int:pk>/', views.DetailExerciceUserView.as_view(), name='exercice_detail_user'),  # User detail view
    path('user/<int:pk>/submit/', views.SoumettreReponseView.as_view(), name='soumettre_reponse'),  # Submit response view
    path('<int:pk>/', views.ExerciceDetailView.as_view(), name='exercice_detail'),
    path('create/', views.ExerciceCreateView.as_view(), name='exercice_create'),
    path('<int:pk>/update/', views.ExerciceUpdateView.as_view(), name='exercice_update'),
    path('<int:pk>/delete/', views.ExerciceDeleteView.as_view(), name='exercice_confirm_delete'),
    
]
