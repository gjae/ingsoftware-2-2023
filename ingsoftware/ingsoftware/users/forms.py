from django import forms
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm

from .models import User, PaymentMethod, PaymentMethodBasedInformation


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingresa tu nombre completo"}),
        required=True,
        label="Nombre completo"
    )


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class UserProfileModelForm(forms.ModelForm):

    email = forms.EmailField(disabled=True, label="Correo electrónico")

    class Meta:
        model = User
        exclude = ["created", "modified", "password", "date_joined", "is_active"]
        readonly_fields = ["email",]


class UserPaymentMethodForm(forms.ModelForm):
    account_note = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Agrega una observación",
        required=False,
        initial=""
    )

    based = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=PaymentMethodBasedInformation.objects.all(),
        label="Banco",
        empty_label="Sin información"
    )

    class Meta:
        model = PaymentMethod
        exclude = ["created", "modified", ]