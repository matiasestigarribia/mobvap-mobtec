from rest_framework import serializers
from .models import Edition


class EditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        fields = ['id', 'edition_name', 'edition_description', 'preview_image1', 'preview_image2', 'created_at', 'updated_at']
