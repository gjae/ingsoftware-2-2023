from django import forms

from tinymce.widgets import TinyMCE
from ingsoftware.campaigns.models import Campaign


class CampaignCreateForm(forms.ModelForm):

    body = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 4}),
        label="Descripción de la campaña",
        required=True
    )

    date_target = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"}),
        label="Fecha de destino",
        help_text="Fecha hasta la cual esta publicación será  mostrada",
        required=True
    )

    def __init__(self, *args, **kwargs):
        title = None
        beneficiary= None
        if "title" in kwargs:
            title = kwargs.get("title", None)
            kwargs.pop("title")

        if "beneficiary" in kwargs:
            beneficiary = kwargs.get("beneficiary", None)
            kwargs.pop("beneficiary")

        super().__init__(*args, **kwargs)

        if title is not None:
            self.fields["title"].initial = title
        
        if beneficiary is not None:
            self.fields["beneficiary"].initial = beneficiary

    class Meta:
        model = Campaign
        exclude = ["created", "modified", "summary", "total_collected", "total_donations", "status"]