from django import forms
from .models import Formulaire, Rapport

class FormulaireForm(forms.ModelForm):
    class Meta:
        model = Formulaire
        fields = ['chapitre', 'contenu', 'type_formulaire', 'note', 'utilisateur']  # Fields to include in the form
        widgets = {
            'chapitre': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Chapitre associé'}),  # Changed to Select
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre retour ici...'}),
            'type_formulaire': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Select(attrs={'class': 'form-control'}),
            'utilisateur': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'chapitre': 'Chapitre associé',
            'contenu': 'Contenu du retour',
            'type_formulaire': 'Type de formulaire',
            'note': 'Note',
            'utilisateur': 'Utilisateur',
        }

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['course', 'formulaire', 'contenu_rapport']  # Champs à inclure dans le formulaire
        widgets = {
            'contenu_rapport': forms.Textarea(attrs={'placeholder': 'Résumé du rapport ici...'}),
        }
        labels = {
            'course': 'Cours associé',
            'formulaire': 'Formulaire lié',
            'contenu_rapport': 'Contenu du rapport',
        }
