from django.shortcuts import render, redirect
from .models import Formulaire, Rapport

def creer_formulaire(request):
    if request.method == 'POST':
        chapitre = request.POST.get('chapitre')
        contenu = request.POST.get('contenu')
        Formulaire.objects.create(chapitre=chapitre, contenu=contenu)
        return redirect('liste_formulaires')
    return render(request, 'satisfaction/creer_formulaire.html')

def liste_formulaires(request):
    formulaires = Formulaire.objects.all()
    return render(request, 'satisfaction/liste_formulaires.html', {'formulaires': formulaires})
