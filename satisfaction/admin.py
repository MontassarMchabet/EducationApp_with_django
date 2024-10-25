from django.contrib import admin
from .models import Formulaire, Rapport

@admin.register(Formulaire)
class FormulaireAdmin(admin.ModelAdmin):
    list_display = ('chapitre', 'date_remplissage', 'type_formulaire', 'note')  # Champs à afficher dans la liste
    search_fields = ('chapitre',)  # Champs pouvant être recherchés
    list_filter = ('type_formulaire',)  # Filtres disponibles dans l'interface d'administration

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('formulaire', 'date_creation')  # Champs à afficher dans la liste
    search_fields = ('formulaire__chapitre',)  # Recherche par chapitre du formulaire associé
