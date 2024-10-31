from django.shortcuts import render, redirect, get_object_or_404
from .models import Examen,QuestionExamen
from .forms import ExamenForm,QuestionExamenForm
from django.contrib import messages
from .utils import TextSummarizer
from django.http import JsonResponse

text_summarizer = TextSummarizer()  # Initialize the summarizer

def examen_list(request):
    examens = Examen.objects.all()
    return render(request, 'examen/examenlist.html', {'examens': examens})

def create_examen(request):
    if request.method == "POST":
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new exam
            messages.success(request, "Examen ajouté avec succès.")
            return redirect('examen_list')  # Redirect after saving
        else:
            print(form.errors)  # Print validation errors for debugging
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")  # Show error message
    else:
        form = ExamenForm()  # Initialize an empty form for GET requests

    return render(request, 'examen/examenlist.html', {'form': form})

def examen_detail(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    return render(request, 'examen/examendetail.html', {'examen': examen})

def update_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)

    if request.method == "POST":
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            messages.success(request, "Examen updated successfully.")
            return redirect('examen_list')  # Redirect to the examen list view
    else:
        form = ExamenForm(instance=examen)  # Initialize the form with the instance of examen

    return render(request, 'examen/examenlist.html', {'form': form})

def delete_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == "POST":
        examen.delete()
        messages.success(request, "Examen deleted successfully.")
        return redirect('examen_list')  # Redirect to the examen list view
    return redirect('examen_list')




def question_list(request):
    # Récupérer toutes les questions
    questions = QuestionExamen.objects.all()  # Récupère toutes les questions

    return render(request, 'questionexamen/listquestion.html', {'questions': questions})



def create_question(request):
    if request.method == "POST":
        form = QuestionExamenForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer la nouvelle question
            messages.success(request, "Question ajoutée avec succès.")
            return redirect('question_list')  # Rediriger après l'enregistrement
        else:
            print(form.errors)  # Afficher les erreurs de validation pour le débogage
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")  # Afficher un message d'erreur
    else:
        form = QuestionExamenForm()  # Initialiser un formulaire vide pour les requêtes GET

    return render(request, 'questionexamen/listquestion.html', {'form': form})

def update_question(request, question_id):
    question = get_object_or_404(QuestionExamen, id=question_id)
    if request.method == "POST":
        form = QuestionExamenForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question mise à jour avec succès.")
            return redirect('question_list', examen_id=question.examen.id)
    else:
        form = QuestionExamenForm(instance=question)
        return render(request, 'questionexamen/listquestion.html', {'form': form})


def delete_question(request, question_id):
    question = get_object_or_404(QuestionExamen, id=question_id)
    if request.method == "POST":
        question.delete()
        messages.success(request, "Question supprimée avec succès.")
        return redirect('question_list')
    return redirect('question_list')


