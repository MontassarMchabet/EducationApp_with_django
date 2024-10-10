
# Echooling.
<div align="center">
 <img src="home/static/assets/images/logo2.png" alt="Elkindy logo">
</div>   
## Résumé de projet
eSchooling est une plateforme éducative intégrant divers modules pour gérer les utilisateurs, les cours, les évaluations et la satisfaction des étudiants. Elle utilise l'IA pour optimiser l'expérience d'apprentissage et faciliter la gestion administrative.

## Aperçu
La plateforme comprend plusieurs modules interconnectés, chacun dédié à des fonctionnalités spécifiques :

1. **Module de gestion des utilisateurs** : Gère les rôles, l'authentification , et inclut un assistant virtuel.
2. **Module de gestion des cours** : Permet la création et la gestion des cours avec assistance IA pour la structure et le contenu.
3. **Module de gestion des évaluations classiques** : Gère les exercices et devoirs avec corrections manuelles et automatiques.
4. **Module de gestion des évaluations chronométrées** : Permet des examens sous contrainte de temps avec correction automatique.
5. **Module de satisfaction des étudiants** : Gère les retours d'expérience avec analyse des tendances et filtrage des réponses.

## Introduction
Echooling vise à améliorer l'apprentissage en ligne en offrant une plateforme conviviale pour les instructeurs et les étudiants. Chaque module est conçu pour répondre à des besoins spécifiques tout en intégrant des outils intelligents pour faciliter l'utilisation et l'efficacité. Grâce à une architecture bien pensée, Echooling assure une gestion fluide des différents aspects de l'éducation.

## Installation
Pour installer Echooling, suivez les étapes ci-dessous :

1. **Cloner le repository :**
   ```bash
   https://github.com/MontassarMchabet/EducationApp_with_django.git
   
   ```
2. **Set Up Environment Variables**: Set up environment variables required for configuration (e.g., database connection details, authentication secrets).
    ```bash
      python -m venv env  
      .\env\Scripts\activate 
    ```
3. **Installer les dépendances :**
   ```bash
      pip install pipenv  # Si Pipenv n'est pas déjà installé
      pipenv install
      pipenv shell
   ```

4. **Configurer la base de données :**
   - Créez une base de données pour le projet et mettez à jour les configurations dans le dossier `env`.
   ```bash
      python manage.py migrate
      python manage.py createsuperuser  # facultatif
   ```

5. **Démarrer le serveur :**
     ```bash
      python manage.py runserver
     ```

6. **Accéder à l'application :**
   Ouvrez votre navigateur et allez à `http://localhost:8000` .
