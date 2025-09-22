from django.contrib import admin
from .models import Edition


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):

    list_display = ('edition_name', 'edition_description', 'preview_image1', 'preview_image2', 'created_at')
    list_filter = ('edition_name',)
    search_fields = ('edition_name', 'created_at')
