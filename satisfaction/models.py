from django.db import models
from django.contrib.auth import get_user_model
from Chapter.models import Chapter
from Course.models import Course

User = get_user_model()  # Get the custom user model

class Formulaire(models.Model):
    TYPE_OPTIONS = [
        ('chapitre', 'Chapitre'),
        ('cours_final', 'Cours Final'),
    ]

    chapitre = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='formulaires')  # Relier au chapitre
    contenu = models.TextField()
    date_remplissage = models.DateTimeField(auto_now_add=True)
    type_formulaire = models.CharField(max_length=20, choices=TYPE_OPTIONS, default='chapitre')  # Set default value
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=1)  # Note par défaut à 1
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formulaires', default=1)  # Set a default user ID

    def __str__(self):
        return f"Formulaire: {self.chapitre.title} - {self.date_remplissage} ({self.type_formulaire}) - Note: {self.note}"

class Rapport(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="rapports")  # Link to Course
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE, related_name="rapports")
    contenu_rapport = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport pour le cours {self.course.title} - {self.date_creation}"