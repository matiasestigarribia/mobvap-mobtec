from django.db import models
from editions.models import Edition
from videos.services import process_video
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class Video(models.Model):
    video_file = models.FileField(upload_to='media/videos/original/')
    video_title = models.CharField(max_length=300)
    video_description = models.TextField(blank=True, null=True)
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT, related_name="videos")
    video_thumbnail = models.ImageField(upload_to='media/videos/thumbnail/', null=True, blank=True)
    thumbnail_display = ImageSpecField(source='video_thumbnail',
                                       processors=[ResizeToFit(400, 400, mat_color="white")],
                                       format='JPEG',
                                       options={'quality': 90})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['video_title']

    def __str__(self):
        return self.video_title

    def save(self, *args, **kwargs):
        if self.pk is None and self.video_file:
            video_to_process = self.video_file

            processed_video_file, thumbnail_file = process_video(video_to_process)

            self.video_file = processed_video_file
            self.video_thumbnail = thumbnail_file

        super().save(*args, **kwargs)
