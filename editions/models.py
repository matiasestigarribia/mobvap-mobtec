from django.db import models
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class Edition(models.Model):
    edition_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
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
        ordering = ['-created_at']

    def __str__(self):
        return self.edition_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.edition_name)
        super().save(*args, **kwargs)
