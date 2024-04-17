from django.utils import timezone
from django.db import models
from django.db.models import F


class CampaignModelManager(models.Manager):


    def list_preview(self, order_by = "-created", *args, **kwargs):
        return (
            super()
            .get_queryset()
            .select_related(
                "user", 
                "category"
            )
            .order_by("-created")
            .filter(date_target__date__gte=timezone.now().date())
            .annotate(
                current_progress=(
                    F("total_collected") * 100 / F("target")
                )
            )
            .values("title", "summary", "target", "id", "created", "current_progress", "img_frontpage", "user_id", "total_collected", "total_donations")
        )