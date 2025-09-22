from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image_file', 'image_title', 'image_description', 'edition', 'created_at')
    list_filter = ('edition',)
    search_fields = ('edition',)
