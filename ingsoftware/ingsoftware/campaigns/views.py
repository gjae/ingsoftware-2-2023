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
from ingsoftware.donatives.models import Donation


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
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = Campaign.objects.filter(pk=self.kwargs.get("pk")).values("user_id").first()

        context["first_donator"] = Donation.objects.filter(campaign_id=self.kwargs.get("pk")).values("mark_as_annonymous", "user__name", "amount").order_by("created").first()
        context["most_important_donator"] = Donation.objects.filter(campaign_id=self.kwargs.get("pk")).values("mark_as_annonymous", "user__name", "amount").order_by("-amount").first()
        context["last_donator"] = Donation.objects.filter(campaign_id=self.kwargs.get("pk")).values("mark_as_annonymous", "user__name", "amount").order_by("created").last()
        
        return context
    

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