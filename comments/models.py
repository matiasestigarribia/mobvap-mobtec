from django.db import models


possible_status = [('approved', 'Approved'), ('pending', 'Pending Review'), ('not_approved', 'Not Approved')]


class Comment(models.Model):
    comment_author = models.CharField(max_length=200)
    comment_text = models.TextField()
    comment_status = models.CharField(max_length=20, choices=possible_status, default='pending')
    azure_safety_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.comment_author} + {self.comment_text[0:15]}"
