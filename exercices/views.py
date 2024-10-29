# exercices/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Exercice, ReponseExercice

# Liste des exercices
class ExerciceListView(ListView):
    model = Exercice
    template_name = 'exercices/exercice_list.html'

# Détail d'un exercice
class ExerciceDetailView(DetailView):
    model = Exercice
    template_name = 'exercices/exercice_detail.html'

# Création d'un exercice
class ExerciceCreateView(CreateView):
    model = Exercice
    fields = ['paragraphe', 'reponse1', 'reponse2', 'reponse3']
    template_name = 'exercices/exercice_create.html'
    success_url = reverse_lazy('exercice_list')

# Mise à jour d'un exercice
class ExerciceUpdateView(UpdateView):
    model = Exercice
    fields = ['paragraphe', 'reponse1', 'reponse2', 'reponse3']
    template_name = 'exercices/exercice_update.html'
    success_url = reverse_lazy('exercice_list')

# Suppression d'un exercice
class ExerciceDeleteView(DeleteView):
    model = Exercice
    template_name = 'exercices/exercice_confirm_delete.html'
    success_url = reverse_lazy('exercice_list')


 #        ////////////////////crud reponse de lexercice  /////////////////

 # exercices/views.py (suite)

# Liste des réponses d'exercices
class ReponseExerciceListView(ListView):
    model = ReponseExercice
    template_name = 'exercices/reponse_list.html'

# Détail d'une réponse d'exercice
class ReponseExerciceDetailView(DetailView):
    model = ReponseExercice
    template_name = 'exercices/reponse_detail.html'

# Création d'une réponse d'exercice
class ReponseExerciceCreateView(CreateView):
    model = ReponseExercice
    fields = ['exercice', 'reponse_etudiant1', 'reponse_etudiant2', 'reponse_etudiant3', 'note']
    template_name = 'exercices/reponse_create.html'
    success_url = reverse_lazy('reponse_list')

# Mise à jour d'une réponse d'exercice
class ReponseExerciceUpdateView(UpdateView):
    model = ReponseExercice
    fields = ['exercice', 'reponse_etudiant1', 'reponse_etudiant2', 'reponse_etudiant3', 'note']
    template_name = 'exercices/reponse_update.html'
    success_url = reverse_lazy('reponse_list')

# Suppression d'une réponse d'exercice
class ReponseExerciceDeleteView(DeleteView):
    model = ReponseExercice
    template_name = 'exercices/reponse_confirm_delete.html'
    success_url = reverse_lazy('reponse_list')
