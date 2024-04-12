from django import forms

from ingsoftware.donatives.models import Donation



class DonativeCreateForm(forms.ModelForm):

    class Meta:
        model = Donation
        exclude = ["created", "modified", ]