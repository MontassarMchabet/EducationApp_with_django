from django.db import models
from Course.models import Course

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')  # Relate to Course
    order = models.IntegerField(default=0)  # To order chapters

    def __str__(self):
        return self.title
