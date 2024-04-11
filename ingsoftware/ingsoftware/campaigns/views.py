from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F

from ingsoftware.campaigns.models import Campaign


class CampaingsListView(ListView):
    template_name = "campaigns/list.html"
    model = Campaign
    queryset = Campaign.objects.list_preview()
    paginate_by = 20
    context_object_name = "campaigns"



class CampaignDetailView(DetailView):
    template_name = "campaigns/detail.html"
    model = Campaign
    queryset = Campaign.objects.select_related()
    context_object_name = "campaign"

    def get_queryset(self):
        return super().get_queryset().annotate(
                current_progress=(
                    F("total_collected") * 100 / F("target")
                )
            )