from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video_file', 'video_title', 'video_thumbnail', 'video_description', 'edition', 'created_at', 'updated_at']
