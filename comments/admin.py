from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('comment_author', 'comment_text', 'comment_status', 'created_at', 'updated_at')
    list_filter = ('comment_status',)
    search_fields = ('comment_author', 'comment_text')
