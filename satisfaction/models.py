from django.db import models
from django.contrib.auth import get_user_model
from Chapter.models import Chapter
from Course.models import Course

User = get_user_model()

class Formulaire(models.Model):
    TYPE_OPTIONS = [
        ('chapitre', 'Chapitre'),
        ('cours_final', 'Cours Final'),
    ]

    chapitre = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='formulaires')
    contenu = models.TextField()
    date_remplissage = models.DateTimeField(auto_now_add=True)
    type_formulaire = models.CharField(max_length=20, choices=TYPE_OPTIONS, default='chapitre')
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=1)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formulaires', null=True, blank=True)

    def __str__(self):
        return f"Formulaire: {self.chapitre.title} - {self.date_remplissage.strftime('%Y-%m-%d %H:%M')} ({self.type_formulaire}) - Note: {self.note}"

class Rapport(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="rapports")
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE, related_name="rapports", null=True, blank=True)
    contenu_rapport = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport pour le cours {self.course.title} - {self.date_creation}"
