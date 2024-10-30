from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('responsable', 'Responsable de Module'),
        ('instructeur', 'Instructeur'),
        ('etudiant', 'Étudiant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')
    
    def __str__(self):
        return self.username