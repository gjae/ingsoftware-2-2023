from django.db import models
from django.contrib.auth import get_user_model
from model_utils.models import TimeStampedModel

from ingsoftware.campaigns.models import Campaign, user_directory_path
from ingsoftware.users.models import PaymentMethod

User = get_user_model()


class Donation(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="donations")
    campaign = models.ForeignKey(Campaign, on_delete=models.RESTRICT, related_name="donatives")
    amount = models.DecimalField("Total donado", decimal_places=2, max_digits=10, default=0.00)

    payed_at = models.DateTimeField("Fecha en la que se realizó la transacción", null=True, default=None)
    voucher = models.FileField(upload_to=user_directory_path, null=True, default=None)
    transaction_code = models.CharField("Codigo de la transaccion", db_index=True, max_length=10, blank=True, default="")
    mark_as_annonymous = models.BooleanField("Marcar donativo como anonimo", default=False)

    payment_method = models.ForeignKey(
        PaymentMethod, 
        on_delete=models.RESTRICT, 
        null=True, 
        default=None, 
        verbose_name="donatives", 
        related_name="donatives"
    )

    class PreventCampaignOwnAutoDonativeException(Exception):
        pass


    def save(self, *args, **kwargs):
        if self.user_id == self.campaign.user_id:
            raise Donation.PreventCampaignOwnAutoDonativeException("El creador de la campaña no puede hacer donativos en su misma campaña")
        
        return super().save(*args, **kwargs)
    

class Comment(TimeStampedModel):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="comment")
    comment = models.CharField("Deja un comentario de apoyo", max_length=250)