from django.dispatch import receiver
from django.db.models.signals import post_save

from ingsoftware.campaigns.models import Campaign

@receiver(post_save, sender=Campaign)
def on_create_campaign_set_model_summary(sender, instance: Campaign, created, *args, **kwargs):
    """
    Cuando un nuevo modelo de Campaign ha sido creado, se modifica el campo summary para que muestre solo
    algunos de los caracteres
    """
    summary = instance.body.lower()[0:70]

    if instance.summary.lower() == summary:
        return None

    instance.summary = summary
    instance.save()