from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Formulaire, Rapport
from .forms import FormulaireForm, RapportForm

class FormulaireListView(ListView):
    model = Formulaire
    template_name = 'satisfaction/formulaire_list.html'
    context_object_name = 'formulaires'

class FormulaireCreateView(CreateView):
    model = Formulaire
    form_class = FormulaireForm
    template_name = 'satisfaction/formulaire_form.html'
    success_url = reverse_lazy('formulaire-list')

    def form_valid(self, form):
        form.instance.utilisateur = self.request.user
        return super().form_valid(form)

class FormulaireUpdateView(UpdateView):
    model = Formulaire
    form_class = FormulaireForm
    template_name = 'satisfaction/formulaire_form.html'
    success_url = reverse_lazy('formulaire-list')

    def get_object(self, queryset=None):
        return get_object_or_404(Formulaire, pk=self.kwargs['pk'])

class FormulaireDeleteView(DeleteView):
    model = Formulaire
    template_name = 'satisfaction/formulaire_confirm_delete.html'
    success_url = reverse_lazy('formulaire-list')

    def get_object(self, queryset=None):
        return get_object_or_404(Formulaire, pk=self.kwargs['pk'])

class RapportListView(ListView):
    model = Rapport
    template_name = 'satisfaction/rapport_list.html'
    context_object_name = 'rapports'

class RapportCreateView(CreateView):
    model = Rapport
    form_class = RapportForm
    template_name = 'satisfaction/rapport_form.html'
    success_url = reverse_lazy('rapport-list')

    def form_valid(self, form):
        course = form.cleaned_data['course']
        formulaire = form.cleaned_data['formulaire']
        contenu_rapport = form.generate_report(course)

        rapport = form.save(commit=False)
        rapport.contenu_rapport = contenu_rapport
        rapport.save()

        return super().form_valid(form)

class RapportUpdateView(UpdateView):
    model = Rapport
    form_class = RapportForm
    template_name = 'satisfaction/rapport_form.html'
    success_url = reverse_lazy('rapport-list')

    def get_object(self, queryset=None):
        return get_object_or_404(Rapport, pk=self.kwargs['pk'])

class RapportDeleteView(DeleteView):
    model = Rapport
    template_name = 'satisfaction/rapport_confirm_delete.html'
    success_url = reverse_lazy('rapport-list')

    def get_object(self, queryset=None):
        return get_object_or_404(Rapport, pk=self.kwargs['pk'])
