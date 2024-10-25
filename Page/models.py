from django.db import models
from Chapter.models import Chapter

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    multimedia = models.FileField(upload_to='uploads/', null=True, blank=True)  # For images/videos
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')  # Relate to Chapter

    def __str__(self):
        return self.title
