from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView, TemplateView, ListView

from ingsoftware.users.models import User

from ingsoftware.campaigns.models import Campaign
from ingsoftware.donatives.models import Donation


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_collected = Campaign.objects.filter(user_id=self.request.user.id).aggregate(total=Sum("total_collected"))
        donated = Donation.objects.filter(user_id=self.request.user.id).aggregate(total=Sum("amount"))
        actives = Campaign.objects.filter(user_id=self.request.user.id, status=Campaign.STATUS.progress).aggregate(total=Count("id"))

        context["total_collected"] = total_collected["total"] if "total" in total_collected and total_collected["total"] is not None else 0.0
        context["total_donated"] = donated["total"] if "total" in donated and donated["total"] is not None else 0.00 
        context["campaign_actives"] = actives["total"] if "total" in actives and actives["total"] is not None else 0



        context["last_donation_receivers"] = Donation.objects.select_related("campaign").filter(campaign__user_id=self.request.user.id).order_by("-created")[0:6]
        context["last_donation_made"] = Donation.objects.select_related("campaign").filter(user_id=self.request.user.id).order_by("-created")[0:6]

        context["bests_campaigns"] = Campaign.objects.list_preview().filter(user_id=self.request.user.id).order_by("-current_progress")[0:3]

        return context
    

class UserCampaignView(LoginRequiredMixin, ListView):
    template_name = "dashboard/campaigns.html"
    model = Campaign
    context_object_name = "campaigns"


    def get_queryset(self):
        return Campaign.objects.list_preview().filter(user_id=self.request.user.id)