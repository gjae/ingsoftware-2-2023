from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from model_utils import Choices
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel
from model_utils.fields import StatusField


from ingsoftware.campaigns.managers import CampaignModelManager

User = get_user_model()
# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.user.id, filename)

class Category(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(
        "Título de la categoría",
        max_length=77,
        db_index=True
    )

    def __str__(self):
        return self.title
    
class Beneficiary(TimeStampedModel):
    Beneficiary = models.CharField(
        "A quien va dirigido"
    )

    alternative_title = models.CharField(
        "Destino de los fondos recaudados",
        max_length=100,
        blank=True,
        default=""
    )

    funds_destination = models.CharField(
        "Destino de los fondos recaudados",
        max_length=100,
        blank=True,
        default=""
    )

    def __str__(self):
        return self.Beneficiary


class Campaign(TimeStampedModel, SoftDeletableModel):
    STATUS = Choices(
        (0, "progress", "En Progreso"),
        (1, "finished", "Finalizada"),
        (2, "canceled", "Cancelada"),
        (3, "draft", "Borrador")
    )
    title = models.CharField(
        "Título de la campaña",
        max_length=95, 
        db_index=True
    )
    summary = models.TextField(
        "Resumen de la campaña",
        blank=True,
        default=""
    )
    body = models.TextField(
        "Descripción de la campaña",
    )
    total_collected = models.DecimalField(
        "Total recaudado",
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    total_donations = models.PositiveBigIntegerField("Donaciones recaudadas", default=0)
    tags = ArrayField(
        models.CharField(max_length=32),
        size=32,
        help_text="Etiquetas de la publicación, ejemplo: tag1,tag2",
        db_index=True,
        verbose_name="Etiquetas de la campaña separadas por coma"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="campaigns", verbose_name="Categoría")
    img_frontpage = models.ImageField(
        "Imagen de portada",
        upload_to=user_directory_path
    )
    target = models.DecimalField(
        "Meta de recaudació",
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    date_target = models.DateTimeField(
        "Fecha limite de recaudación",
        null=True,
        default=None
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campaigns")
    status = models.IntegerField(choices=STATUS, default=STATUS.draft)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="campaigns", verbose_name="Beneficiario")

    objects = CampaignModelManager()


class CampaignUserFollowing(TimeStampedModel, SoftDeletableModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campaigns_follows")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="user_followers")