

# Create your models here.
# exercices/models.py
from django.db import models

class Exercice(models.Model):
    paragraphe = models.TextField()  # Texte du paragraphe avec des trous
    reponse1 = models.CharField(max_length=100)  # Première réponse attendue
    reponse2 = models.CharField(max_length=100)  # Deuxième réponse attendue
    reponse3 = models.CharField(max_length=100)  # Troisième réponse attendue
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exercice {self.id}"

class ReponseExercice(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)  # Lien vers Exercice
    reponse_etudiant1 = models.CharField(max_length=100)  # Première réponse soumise
    reponse_etudiant2 = models.CharField(max_length=100)  # Deuxième réponse soumise
    reponse_etudiant3 = models.CharField(max_length=100)  # Troisième réponse soumise
    note = models.FloatField(null=True, blank=True)  # Note (calculée si nécessaire)
    date_reponse = models.DateTimeField(auto_now_add=True)  # Date de soumission de la réponse

    def __str__(self):
        return f"Réponse pour Exercice {self.exercice.id}"
