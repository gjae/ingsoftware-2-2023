from django.apps import AppConfig
import contextlib


class CampaignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingsoftware.campaigns'

    def ready(self):
        with contextlib.suppress(ImportError):
            import ingsoftware.campaigns.signals  # noqa: F401
