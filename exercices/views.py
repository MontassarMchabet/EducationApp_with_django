# exercices/views.py
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Exercice, ReponseExercice
from .utils import valider_reponse  # Importer la fonction de validation

# Liste des exercices
class ExerciceListView(ListView):
    model = Exercice
    template_name = 'exercices/exercice_list.html'
    context_object_name = 'exercices'

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

    #///////////////////

 # Liste des exercices pour l'utilisateur avec bouton "passer"
class ExerciceListUserView(ListView):
    model = Exercice
    template_name = 'exercices/exercice_list_user.html'
    context_object_name = 'exercices'

# Affichage de l'exercice pour l'utilisateur
class DetailExerciceUserView(View):
    template_name = 'exercices/exercice_detail_user.html'
    
    def get(self, request, pk):
        exercice = get_object_or_404(Exercice, pk=pk)
        return render(request, self.template_name, {'exercice': exercice})

class SoumettreReponseView(View):
    def post(self, request, pk):
        exercice = get_object_or_404(Exercice, pk=pk)
        reponse1 = request.POST.get('reponse1')
        reponse2 = request.POST.get('reponse2')
        reponse3 = request.POST.get('reponse3')

        # Calcul de la note en utilisant valider_reponse pour comparer chaque réponse
        note = sum([
            valider_reponse(reponse1, exercice.reponse1),
            valider_reponse(reponse2, exercice.reponse2),
            valider_reponse(reponse3, exercice.reponse3)
        ]) / 3 * 100

        # Enregistrement de la réponse
        reponse = ReponseExercice.objects.create(
            exercice=exercice,
            reponse_etudiant1=reponse1,
            reponse_etudiant2=reponse2,
            reponse_etudiant3=reponse3,
            note=note
        )

        # Redirection vers la vue d'affichage de la note
        return redirect('afficher_note', pk=exercice.id)
    

# exercices/views.py

class AfficherNoteView(View):
    template_name = 'exercices/afficher_note.html'  # Chemin vers le template d'affichage de la note
    
    def get(self, request, pk):
        # Obtenez la dernière réponse soumise par l'étudiant pour l'exercice donné
        reponse = ReponseExercice.objects.filter(exercice__id=pk).order_by('-id').first()
        
        # Vérifiez si une réponse a été trouvée
        if reponse is None:
            return redirect('exercice_list_user')  # Redirigez si aucune réponse n'existe
        
        return render(request, self.template_name, {'reponse': reponse})
