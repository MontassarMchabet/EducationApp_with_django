from django.db import models

class Formulaire(models.Model):
    TYPE_OPTIONS = [
        ('chapitre', 'Chapitre'),
        ('cours_final', 'Cours Final'),
    ]

    chapitre = models.CharField(max_length=255)
    contenu = models.TextField()
    date_remplissage = models.DateTimeField(auto_now_add=True)
    type_formulaire = models.CharField(max_length=20, choices=TYPE_OPTIONS)
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=1)  # Note par défaut à 1

    def __str__(self):
        return f"Formulaire: {self.chapitre} - {self.date_remplissage} ({self.type_formulaire}) - Note: {self.note}"
class Rapport(models.Model):
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE, related_name="rapports")
    contenu_rapport = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport pour {self.formulaire.chapitre} - {self.date_creation}"
