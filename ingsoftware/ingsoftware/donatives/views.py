from django.urls import reverse_lazy
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import error

from .forms import DonativeCreateForm, CommentCreateForm
from ingsoftware.campaigns.models import Campaign
from ingsoftware.donatives.models import Donation

class DonativeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "donatives/create.html"
    form_class = DonativeCreateForm
    success_message = "Gracias por su donación, estamos procesandola"
    success_url = reverse_lazy("campaigns.list")

    def get_campaign_object(self):
        return Campaign.objects.filter(pk=self.kwargs.get("pk")).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context["campaign"] = self.get_campaign_object()
        return context
    
    def get(self, request, *args, **kwargs):
        if self.get_campaign_object() is None:
            return HttpResponseNotFound()

        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = None
        try:
            response = super().form_valid(form)
            if "comment" in self.request.POST and self.request.POST.get("comment", "-") != "-":
                initial = self.request.POST.copy()
                initial["donation"] = self.object.id
                print(initial)
                comment_form = CommentCreateForm(initial)
                comment_form.is_valid()
                comment_form.save()

        except Donation.PreventCampaignOwnAutoDonativeException as e:
            error(self.request, str(e))
            return HttpResponseRedirect(self.request.META["HTTP_REFERER"])

        return response