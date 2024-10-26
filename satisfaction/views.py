from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Formulaire, Rapport
from .forms import FormulaireForm, RapportForm

# Vue pour lister tous les formulaires
class FormulaireListView(ListView):
    model = Formulaire
    template_name = 'satisfaction/formulaire_list.html'  # Assurez-vous que le chemin correspond à la structure de vos templates
    context_object_name = 'formulaires'  # Nom du contexte pour accéder aux formulaires dans le template

# Vue pour créer un nouveau formulaire
class FormulaireCreateView(CreateView):
    model = Formulaire
    form_class = FormulaireForm
    template_name = 'satisfaction/formulaire_form.html'  # Assurez-vous que le chemin correspond à la structure de vos templates
    success_url = reverse_lazy('formulaire-list')  # Redirige vers la liste après création

    def form_valid(self, form):
        form.instance.utilisateur = self.request.user  # Associe l'utilisateur connecté au formulaire
        return super().form_valid(form)

# Vue pour lister tous les rapports
class RapportListView(ListView):
    model = Rapport
    template_name = 'satisfaction/rapport_list.html'  # Assurez-vous que le chemin correspond à la structure de vos templates
    context_object_name = 'rapports'  # Nom du contexte pour accéder aux rapports dans le template

# Vue pour créer un nouveau rapport
class RapportCreateView(CreateView):
    model = Rapport
    form_class = RapportForm
    template_name = 'satisfaction/rapport_form.html'  # Assurez-vous que le chemin correspond à la structure de vos templates
    success_url = reverse_lazy('rapport-list')  # Redirige vers la liste après création
