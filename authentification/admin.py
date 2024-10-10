from django.contrib import admin
from .models import User  # Assurez-vous que votre modèle User est importé

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')  # Affichez les champs que vous voulez dans l'administration
    search_fields = ('username', 'email')  # Ajoutez des champs pour la recherche
