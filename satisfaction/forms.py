from django import forms
from .models import Formulaire, Rapport

class FormulaireForm(forms.ModelForm):
    class Meta:
        model = Formulaire
        fields = ['chapitre', 'contenu', 'type_formulaire', 'note', 'utilisateur']  # Champs à inclure dans le formulaire
        widgets = {
            'contenu': forms.Textarea(attrs={'placeholder': 'Votre retour ici...'}),
            'type_formulaire': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Select(attrs={'class': 'form-select'}),
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
