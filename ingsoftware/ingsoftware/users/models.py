
from typing import ClassVar
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils import Choices

from .managers import UserManager


PAYMENT_METHOD_CHOICES = Choices(
    (0, "pm", "Pagomovil"),
    (1, "ti", "Transferencia Interbancaria"),
    (2, "tt", "Transferecia bancaria"),
    (3, "div", "Divisas"),
    (4, "tdiv", "Transferencia de divisas electronicas"),
    (5, "otr", "Otras"),
)

class User(AbstractUser):
    """
    Default custom user model for My Awesome Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})



class PaymentMethodBasedInformation(TimeStampedModel):
    bank = models.CharField("Banco", max_length=32)
    code = models.CharField("Codigo del metodo", max_length=17, db_index=True)
    icon = models.ImageField("Imagen del metodo", upload_to="assets/")

    def __str__(self):
        return f"{self.code} - {self.bank}"


class PaymentMethod(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
    card_id = models.PositiveIntegerField()
    payment_method = models.PositiveIntegerField(choices=PAYMENT_METHOD_CHOICES)
    account_named = models.CharField("Titular de la cuenta", max_length=85)
    account_number = models.CharField("Número de cuenta", max_length=100, db_index=True)
    based = models.ForeignKey(PaymentMethodBasedInformation, on_delete=models.RESTRICT, related_name="payment_methods")


