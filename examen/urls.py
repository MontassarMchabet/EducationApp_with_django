from django.urls import path
from .views import examen_list, create_examen, update_examen, delete_examen, examen_detail,question_list,create_question,update_question,delete_question

urlpatterns = [
    path('', examen_list, name='examen_list'),  # List of exams
    path('create/', create_examen, name='create_examen'),  # Create a new exam
    path('update/<int:pk>/', update_examen, name='update_examen'),  # Update an exam
    path('delete/<int:pk>/', delete_examen, name='delete_examen'),  # Delete an exam
    path('exams/<int:examen_id>/', examen_detail, name='examen_detail'),  # URL for exam details

 # URL pour les questions associées à un examen
    path('questions/', question_list, name='question_list'),  # Liste des questions
        path('create/question', create_question, name='create_question'),

    path('updatequestion/<int:question_id>/', update_question, name='update_question'),  # Mettre à jour une question
    path('deletequestion/<int:question_id>/', delete_question, name='delete_question'),  # Supprimer une question


]
