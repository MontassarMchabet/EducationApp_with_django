from django.db import models

class Course(models.Model):
    COURSE_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    course_level = models.CharField(max_length=12, choices=COURSE_LEVEL_CHOICES)
    number_of_chapters = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in hours")

    def __str__(self):
        return self.title
