from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives

from ingsoftware.donatives.models import Donation


@receiver(post_save, sender=Donation)
def on_donative_received_set_campaign_stats(sender, instance: Donation, created, *args, **kwargs):

    print("Calculando nuevos stats")
    if instance.amount <= 0.0:
        return False
    
    campaign = instance.campaign

    campaign.total_collected = campaign.total_collected + instance.amount
    campaign.total_donations = campaign.total_donations + 1
    campaign.save()
    print("Nuevos stats calculados")