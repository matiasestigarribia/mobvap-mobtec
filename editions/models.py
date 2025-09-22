from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class Edition(models.Model):
    edition_name = models.CharField(max_length=200, unique=True)
    edition_description = models.TextField()
    preview_image1 = ProcessedImageField(upload_to='media/editions/previews/',
                                         processors=[ResizeToFit(400, 400, mat_color="white")],
                                         format='JPEG',
                                         options={'quality': 90})
    preview_image2 = ProcessedImageField(upload_to='media/editions/previews/',
                                         processors=[ResizeToFit(400, 400, mat_color="white")],
                                         format='JPEG',
                                         options={'quality': 90})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['edition_name']

    def __str__(self):
        return self.edition_name
