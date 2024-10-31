import requests
from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('responsable', 'Responsable de Module'),
        ('instructeur', 'Instructeur'),
        ('etudiant', 'Étudiant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def generate_avatar(self):
        # Utiliser l'API DiceBear pour générer un avatar à partir du nom d'utilisateur
        avatar_url = f'https://api.dicebear.com/9.x/adventurer/svg?seed={self.username}'
        try:
            response = requests.get(avatar_url)
            response.raise_for_status()  # Vérifie les erreurs de requête

            # Charger l'image depuis la réponse
            image_content = BytesIO(response.content)
            # Enregistrer l'image dans le champ profile_image
            self.profile_image.save(f'{self.username}_avatar.png', File(image_content), save=True)
            print('Avatar sauvegardé avec succès pour:', self.username)  # Ajout pour le débogage
        except requests.exceptions.HTTPError as err:
            print('Erreur lors de la récupération de l\'avatar:', err)
        except Exception as e:
            print('Erreur lors de la sauvegarde de l\'avatar:', e)


    def __str__(self):
        return self.username
