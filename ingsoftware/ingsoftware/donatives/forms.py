from django import forms

from ingsoftware.donatives.models import Donation, Comment


class DonativeCreateForm(forms.ModelForm):
    payed_at = forms.DateTimeField(
        widget=forms.TextInput(attrs={"type": "date"}),
        label="Fecha en la que se realizó la transacción",
        required=True
    )

    class Meta:
        model = Donation
        exclude = ["created", "modified", ]

class CommentCreateForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        initial="-"
    )

    class Meta:
        model = Comment
        fields = ["comment", "donation"]