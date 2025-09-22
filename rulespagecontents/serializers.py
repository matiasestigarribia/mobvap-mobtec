from rest_framework import serializers
from .models import RulesPageContent


class RulesPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RulesPageContent
        fields = ['id', 'rules_title', 'rules_text', 'featured_image', 'created_at', 'updated_at']
