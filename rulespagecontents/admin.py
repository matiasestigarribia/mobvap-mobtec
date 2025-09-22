from django.contrib import admin
from .models import RulesPageContent


@admin.register(RulesPageContent)
class RulesPageContentAdmin(admin.ModelAdmin):
    list_display = ('rules_title', 'rules_text', 'pdf_file_mobvap', 'pdf_file_mobtec', 'created_at')
    list_filter = ('rules_title',)
    search_fields = ('rules_title',)
