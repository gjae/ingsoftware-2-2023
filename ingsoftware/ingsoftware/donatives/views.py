from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .forms import DonativeCreateForm

class DonativeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "donatives/create.html"
    form_class = DonativeCreateForm
    success_message = "Gracias por su donación, estamos procesandola"
    success_url = reverse_lazy("campaigns.list")