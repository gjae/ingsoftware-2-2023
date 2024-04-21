from typing import Any
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.http.response import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView, TemplateView, ListView, FormView, DeleteView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.base import ContextMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import success
from django.contrib.auth.forms import PasswordChangeForm


from ingsoftware.users.models import User, PaymentMethod

from ingsoftware.campaigns.models import Campaign
from ingsoftware.donatives.models import Donation
from .forms import UserProfileModelForm, UserPaymentMethodForm


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
    

class CancelCampaignView(LoginRequiredMixin, DeleteView):
    def get_success_url(self) -> str:
        return reverse("users:dashboard.campaigns")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        campaign = Campaign.objects.filter(user_id=self.request.user.id, id=int(self.request.POST.get("pk")))

        if campaign is None:
            return HttpResponseBadRequest()
        

        campaign.update(status=Campaign.STATUS.canceled)
        success(self.request, "La campaña fue cancelada")
        return HttpResponseRedirect(self.get_success_url())
    

class UserDonationsView(LoginRequiredMixin, ListView):
    template_name = "dashboard/donations.html"
    model = Campaign
    context_object_name = "donations"


    def get_queryset(self):
        return Donation.objects.select_related().filter(user_id=self.request.user.id)
    


class ProfileSettinMixin(ContextMixin):
    template_name = "dashboard/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form_view"] = UserProfileModelForm(initial={
            "name": self.request.user.name,
            "email": self.request.user.email,
            "phone_number": self.request.user.phone_number,
            "alternative_phone": self.request.user.alternative_phone,
            "address": self.request.user.address,
            "card_id": self.request.user.card_id,
            "profile_photo": self.request.user.profile_photo
        })

        context["payment_methods"] = (
            PaymentMethod
            .objects
            .filter(user_id=self.request.user.id)
            .select_related("based")
            .annotate(
                qtty_donatives_using=Count("donatives")
            )
        )


        return context
    


class ProfileUserView(LoginRequiredMixin, ProfileSettinMixin,  TemplateView):
    pass


class ProfileUserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserProfileModelForm
    model = User
    success_message = "Su perfil de usuario ha sido correctamente actualizado"

    def get_success_url(self) -> str:
        return self.request.META.get("HTTP_REFERER")
    

class ProfileChangePasswordForm(LoginRequiredMixin, SuccessMessageMixin,  ProfileSettinMixin, FormView):
    form_class = PasswordChangeForm
    model = User
    success_message = "Su perfil de usuario ha sido correctamente actualizado"

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()

        form = form_class(self.request.user, **self.get_form_kwargs())
        return form
    
    def form_valid(self, form):
        form.save()

        return HttpResponseRedirect(reverse("account_login"))
    
    def get_success_url(self) -> str:
        print("URL ", self.request.META.get("HTTP_REFERER"))
        return self.request.META.get("HTTP_REFERER")
    
    

class PaymentMethodCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "dashboard/payment_methods/create.html"
    form_class = UserPaymentMethodForm
    success_message = "Su nueva cuenta %(account_number)s fue correctamente creada. Ahora podra ser elegible en sus campañas"

    def get_success_url(self) -> str:
        return reverse("users:dashboard.profile")
    

class PaymentMethodUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/payment_methods/create.html"
    form_class = UserPaymentMethodForm
    success_message = "Su nueva cuenta %(account_number)s fue correctamente actualizada."
    queryset = PaymentMethod.objects.select_related()

    def get_success_url(self) -> str:
        return reverse("users:dashboard.profile")
    

class PaymentMethodDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "dashboard/payment_methods/create.html"
    form_class = UserPaymentMethodForm
    queryset = PaymentMethod.objects.select_related()

    def get_success_url(self) -> str:
        return reverse("users:dashboard.profile")
    


    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print(request.POST)
        method = PaymentMethod.objects.filter(user_id=self.request.user.id, id=int(self.request.POST.get("pk"))).annotate(
            qtty_donatives_using=Count("donatives")
        ).first()

        if method is None:
            return HttpResponseBadRequest()
        
        if method.qtty_donatives_using > 0:
            return HttpResponseBadRequest()

        method.delete()
        success(self.request, "El metodo de pago fue eliminado exitosamente")
        return HttpResponseRedirect(self.get_success_url())