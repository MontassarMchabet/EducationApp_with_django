
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from django.core.files.base import ContentFile
from .models import User
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm
import base64
import requests
import logging
from .forms import UserProfileForm

# Initialiser le logger
logger = logging.getLogger('app')
FACE_API_URL = 'https://api-us.faceplusplus.com/facepp/v3/compare'
api_key = 'TcUNlfoFoLqkzPrC0zz8vGu1Qodk4VLB'
api_secret = '5vQtsxII3O5KicWSmG8IMcbO0PLFqq5H'


def compare_faces(image_data1, image_data2):
    """Compare deux images avec l'API Face++."""
    logger.debug("Début de la comparaison des visages avec l'API Face++")
   
    params = {'api_key': 'TcUNlfoFoLqkzPrC0zz8vGu1Qodk4VLB', 
    'api_secret' : '5vQtsxII3O5KicWSmG8IMcbO0PLFqq5H', 
    'image_base64_1' : image_data1, 
    'image_base64_2' : image_data2
    }
    api_url = 'https://api-us.faceplusplus.com/facepp/v3/compare'
    try:
        ''' response = requests.post(FACE_API_URL, files=files) '''
        r = requests.post(api_url, params)
        r.raise_for_status()  # Lève une exception pour les erreurs HTTP
        result = r.json()
        logger.debug(f"Réponse de l'API Face++ : {result}")
        return result.get('confidence', 0) > 80
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de l'appel à l'API Face++ : {e}")
        return False

def login_view2(request):
    if request.method == 'POST':
        # Récupération de l'image de connexion en base64
        login_image_data = request.POST.get('login_image_data')
        
        if not login_image_data:
            messages.error(request, "Image de connexion manquante.")
            return render(request, 'login2.html')
        
        # Recherche de l'utilisateur par reconnaissance faciale
        for user in User.objects.all():
            logger.warning(f"{user.profile_image}")
            if user.profile_image:
                profile_image_content = user.profile_image.read()
                profile_image_data = base64.b64encode(profile_image_content).decode('utf-8')
                
                # Comparer les images avec l'API Face++
                if compare_faces(login_image_data, profile_image_data):
                    logger.debug(f"Comparaison faciale réussie pour l'utilisateur : {user.username}")
                    login(request, user)
                    messages.success(request, f'Bienvenue, {user.role} !')
                    return redirect('StudentHome') if user.role == 'etudiant' else redirect('InstructorsHome')
        
        # Si aucun utilisateur ne correspond
        logger.warning("Comparaison faciale échouée pour tous les utilisateurs")
        messages.error(request, 'La reconnaissance faciale a échoué ou l’utilisateur n’existe pas.')
    
    return render(request, 'login2.html')



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Gestion de l'image capturée en base64
            profile_image_data = request.POST.get('profile_image_data')
            if profile_image_data:
                # Décoder l'image base64
                format, imgstr = profile_image_data.split(';base64,') 
                ext = format.split('/')[-1] 
                # Créer le fichier d'image
                user.profile_image.save(f'{user.username}_profile.{ext}', ContentFile(base64.b64decode(imgstr)), save=False)

            user.save()
            messages.success(request, "Votre compte a été créé avec succès!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print('username:',username)
            password = form.cleaned_data.get('password')
            print('password:', password)
            user = authenticate(request, username=username, password=password)
            
            # Affichage pour debug dans la console
            print('Utilisateur authentifié :', user)
            
            if user is not None:
                login(request, user)
                print('Utilisateur connecté :', user)
                
                # Vérification du rôle de l'utilisateur pour la redirection
                if user.is_superuser:
                    messages.success(request, 'Bienvenue, super utilisateur !')
                    return redirect('/admin/')  # Redirection vers le dashboard admin
                elif user.role == 'responsable':
                    messages.success(request, 'Bienvenue, responsable de module !')
                    return redirect('home')  # Redirection vers le tableau de bord du responsable
                elif user.role == 'instructeur':
                    messages.success(request, 'Bienvenue, instructeur !')
                    return redirect('InstructorsHome')  # Redirection vers le tableau de bord instructeur
                else:
                    messages.success(request, 'Bienvenue, étudiant !')
                    return redirect('course_list')  # Redirection vers le tableau de bord de l'étudiant
            else:
                # Afficher un message si l'authentification échoue
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Redirige vers le profil après la mise à jour
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'profile.html', {'form': user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('profile')  # Redirection vers la page du profil
    else:
        form = UpdateProfileForm(instance=request.user)
    
    return render(request, 'profile/update_profile.html', {'form': form})
@login_required
def home(request):
    return render(request, 'coureses-grid.html')
@login_required
def InstructorsHome(request):
    return render(request, 'instructors.html')
@login_required
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('index')