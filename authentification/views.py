
# from django.shortcuts import render, redirect
# from django.contrib.auth import login , authenticate
# from django.contrib import messages
# from django.contrib.auth.views import LoginView
# from .forms import CustomUserCreationForm, LoginForm
# from .models import User
# from django.contrib.auth.decorators import login_required
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # Redirige vers la page d'accueil après l'inscription
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'signup.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             print('aa',user)
#             # if user is not None:
#             #     login(request, user)
#             #     if user.is_superuser:
#             #         return redirect('/admin/')  # Redirection vers le dashboard admin
#             #     else:
#             #         return redirect('register')  # Redirection vers le tableau de bord utilisateur
#             if user is not None:
#                 login(request, user)
#                 print(user)
#                 if user.is_superuser:
#                     messages.error(request, 'user is super user')
#                     return redirect('/admin/')
#                 else:
#                     print('BB')
#                     messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
#                     return redirect('home')
                    
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# @login_required
# def home(request):
#     return render(request, 'coureses-grid.html')
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from .models import User
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print('form:',form)
        if form.is_valid():
            form.save()
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
                    return redirect('StudentHome')  # Redirection vers le tableau de bord de l'étudiant
            else:
                # Afficher un message si l'authentification échoue
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

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