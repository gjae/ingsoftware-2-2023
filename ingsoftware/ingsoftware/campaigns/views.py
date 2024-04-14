from typing import Any
from django.urls import reverse
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F

from ingsoftware.campaigns.models import Campaign
from ingsoftware.campaigns.forms import CampaignCreateForm


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
    

class CreateCampaignFormView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "campaigns/create.html"
    model = Campaign
    form_class = CampaignCreateForm
    success_message = "Su nueva campaña ha sido correctamente creada"

    def get_success_url(self) -> str:
        return reverse("campaign.details", kwargs={"pk": self.object.pk})
    

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["title"] = self.request.GET.get("title", None)
        kwargs["beneficiary"] = self.request.GET.get("beneficiary", None)
        return kwargs