from django.db import models


class HomePageContent(models.Model):
    home_title = models.CharField(max_length=200)
    youtube_url = models.URLField(max_length=300)
    block_content1_title = models.CharField(max_length=200)
    block_content1_text = models.TextField()
    youtube_url2 = models.URLField(max_length=300, blank=True, null=True)
    block_content2_title = models.CharField(max_length=200)
    block_content2_text = models.TextField()
    schedule_table_title = models.CharField(null=True, blank=True)
    schedule_table_html = models.TextField()
    block_content3_title = models.CharField(max_length=200)
    block_content3_text = models.TextField()
    block_content4_title = models.CharField(max_length=200, blank=True, default=".")
    block_content4_text = models.TextField(blank=True, null=True, default=".")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self):
        return self.home_title
