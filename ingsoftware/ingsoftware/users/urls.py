from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view
from .views import (
    UserDashboardView,
    UserCampaignView,
    UserDonationsView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard.home"),
    path("dashboard/campagins", UserCampaignView.as_view(), name="dashboard.campaigns"),
    path("dashboard/donations/", UserDonationsView.as_view(), name="dashboard.donations"),
]
