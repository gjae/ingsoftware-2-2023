import contextlib
from django.apps import AppConfig


class DonativesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingsoftware.donatives'


    def ready(self):
        with contextlib.suppress(ImportError):
            import ingsoftware.donatives.signals  # noqa: F401
