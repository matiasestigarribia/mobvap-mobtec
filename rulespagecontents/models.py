from django.db import models


class RulesPageContent(models.Model):
    rules_title = models.CharField(max_length=200)
    rules_text = models.TextField()
    pdf_file_mobvap = models.FileField(
        upload_to='rules/pdfs/', 
        null=True, 
        blank=True
    )
    pdf_file_mobtec = models.FileField(
        upload_to='rules/pdfs/', 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Rules Page Contents"

    def __str__(self):
        return self.rules_title
