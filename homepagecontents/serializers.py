from rest_framework import serializers
from .models import HomePageContent


class HomePageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageContent
        fields = ['id', 'home_title', 'youtube_url', 'block_content1_title', 'block_content1_text',
                  'youtube_url2', 'block_content2_title', 'block_content2_text', 'schedule_table_html',
                  'block_content3_title', 'block_content3_text', 'block_content4_title', 'block_content4_text', 'created_at', 'updated_at']
