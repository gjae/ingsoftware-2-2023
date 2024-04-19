from django.conf import settings
from datetime import datetime
from config import celery_app
from django.core.mail import EmailMultiAlternatives

from .models import Campaign


@celery_app.task()
def check_expires_campaigns():
    now = datetime.now()
    camps = Campaign.objects.select_related("user").filter(date_target__date__lte=now.date(), status=Campaign.STATUS.progress)
    

    for camp in camps:
        url = f"{settings.APP_URL}/campaigns/{camp.id}/"
        subject, from_email, to = "Campaña expirada", "noreply@fundve.xyz", camp.user.email
        html_content = (
            f"Hola {camp.user.name}! le notificamos que su campaña <strong>({camp.title})</strong>  (<a href='{url}'>{url}</a>) "
            "Ha llegado a su fecha tope de recaudación, por lo que saldrá del listado de campañas activas. Podra seguir recibiendo donativos mediante el enlace permanente hasta questa sea cancelada. "
        )
        msg = EmailMultiAlternatives(subject, "", from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    camps.update(status=Campaign.STATUS.finished)



@celery_app.task()
def check_target_completeds():
    camps = Campaign.objects.list_completed_targets().select_related("user")


    for camp in camps:
        url = f"{settings.APP_URL}/campaigns/{camp.id}/"
        subject, from_email, to = "Objetivo alcanzado!", "noreply@fundve.xyz", camp.user.email
        html_content = (
            f"Hola {camp.user.name}! le notificamos que su objetivo de recolección para la campaña <strong>({camp.title})</strong>  (<a href='{url}'>{url}</a>) "
            "Ha llegado a su meta de recaudación. Felicidades por ésta hazaña que ha motivado a muchas personas! "
        )
        msg = EmailMultiAlternatives(subject, "", from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    
    camps.update(target_achieved_notified_at=datetime.now())