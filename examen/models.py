from django.db import models

class Examen(models.Model):
    EXAM_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('oral', 'Oral'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")  # Durée en minutes
    number_of_questions = models.IntegerField()
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Minimum score to pass")
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)


    def __str__(self):
        return self.title



class QuestionExamen(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice Question'),
        ('open', 'Open-ended Question'),
        ('true_false', 'True/False'),
    ]

    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    options = models.JSONField(blank=True, null=True, help_text="For MCQ, store options as JSON")
    correct_answer = models.TextField(help_text="Correct answer or correct option for MCQ")
    points = models.DecimalField(max_digits=5, decimal_places=2, help_text="Points for this question")

    def __str__(self):
        return f"Question for {self.examen.title}"
