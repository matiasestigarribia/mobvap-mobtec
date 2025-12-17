import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .services import moderate_comment


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Comment)
def moderate_comment_on_save(sender, instance, created, **kwargs):
    if created:
        try:
            final_status, analysis_data = moderate_comment(instance.comment_text)

            instance.comment_status = final_status
            instance.azure_safety_response = analysis_data

            instance.save(update_fields=['comment_status', 'azure_safety_response'])
        except Exception as e:
            logger.error(f'Error on comments signal: {e}')
            pass