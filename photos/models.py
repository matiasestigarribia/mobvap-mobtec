from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from editions.models import Edition


class Photo(models.Model):
    image_file = ProcessedImageField(upload_to='media/photos/processed/',
                                     processors=[ResizeToFit(1200, 1200, mat_color="white")],
                                     format='JPEG',
                                     options={'quality': 90})

    image_title = models.CharField(max_length=200)
    image_description = models.TextField(blank=True, null=True)
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT, related_name='photos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['edition']

    def __str__(self):
        return self.image_title
