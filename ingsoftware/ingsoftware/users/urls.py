from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view
from .views import (
    UserDashboardView,
    UserCampaignView,
    CancelCampaignView,
    UserDonationsView,
    ProfileUserView,
    ProfileUserUpdateView,
    ProfileChangePasswordForm,
    PaymentMethodCreateView,
    PaymentMethodUpdateView,
    PaymentMethodDeleteView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard.home"),
    path("dashboard/campagins", UserCampaignView.as_view(), name="dashboard.campaigns"),
    path("dashboard/campaigns/cancel/", CancelCampaignView.as_view(), name="dashboard.campaigns.cancel"),
    path("dashboard/donations/", UserDonationsView.as_view(), name="dashboard.donations"),
    path("dashboard/profile/", ProfileUserView.as_view(), name="dashboard.profile"),
    path("dashboard/profile/<int:pk>/update/", ProfileUserUpdateView.as_view(), name="dashboard.profile.update"),
    path("dashboard/profile/<int:pk>/update/password/", ProfileChangePasswordForm.as_view(), name="dashboard.profile.update_password"),
    path("dashboard/profile/pa/create/", PaymentMethodCreateView.as_view(), name="dashboard.profile.payment_methods.create"),
    path("dashboard/profile/pa/<int:pk>/edit", PaymentMethodUpdateView.as_view(), name="dashboard.profile.payment_methods.edit"),
    path("dashboard/profile/pa/delete/", PaymentMethodDeleteView.as_view(), name="dashboard.profile.payment_method.delete"),
]
