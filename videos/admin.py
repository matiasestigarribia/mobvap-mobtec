from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('video_file', 'video_title', 'video_description','edition',
                    'video_thumbnail', 'created_at')
    list_filter = ('edition',)
    search_fields = ('edition',)
