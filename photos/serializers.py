from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image_file', 'image_title', 'image_description', 'edition', 'created_at', 'updated_at']
