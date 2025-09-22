from django.contrib import admin
from .models import HomePageContent


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('home_title', 'youtube_url', 'block_content1_title',
                    'block_content1_text', 'youtube_url2', 'block_content2_title',
                    'block_content2_text', 'schedule_table_html', 'block_content3_title',
                    'block_content3_text', 'created_at', 'updated_at')
    list_filter = ('home_title', 'block_content1_title', 'block_content2_title',
                   'block_content3_title', 'created_at')
    search_fields = ('home_title', 'block_content1_title', 'block_content2_title',
                     'block_content3_title', 'created_at')
