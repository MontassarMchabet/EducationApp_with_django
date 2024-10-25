from django.urls import path
from . import views

urlpatterns = [
    path('creer/', views.creer_formulaire, name='creer_formulaire'),
    path('', views.liste_formulaires, name='liste_formulaires'),
]
