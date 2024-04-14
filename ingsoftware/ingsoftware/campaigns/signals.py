from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


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

@receiver(post_save, sender=Campaign)
def on_create_campaign_send_confirmation_email(sender, instance: Campaign, created, *args, **kwargs):
    if not created:
        return False
    

    user =instance.user

    subject = f"Tu campaña ha sido creada"
    subject, from_email, to = f"Tu campaña ha sido creada", "noreply@fundve.xyz", user.email
    text_content = "This is an important message."
    html_content = (
        f"Hola {user.name}! te notificamos que tu nueva campaña <strong>({instance.title})</strong> "
        "ha sido correctamente creada y está lista para comenzar a recaudar fondos; te deseamos suerte!."
    )
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()