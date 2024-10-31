from django import forms
from .models import Examen,QuestionExamen

class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = [
            'title',
            'description',
            'duration',
            'number_of_questions',
            'passing_score',
            'exam_type',

        ]


class QuestionExamenForm(forms.ModelForm):
    class Meta:
        model = QuestionExamen
        fields = [
      
            'question_text',
            'question_type',
            'options',
            'correct_answer',
            'points',
        ]

