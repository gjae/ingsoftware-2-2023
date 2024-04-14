from django.urls import path, include

from ingsoftware.campaigns import views


urlpatterns = [
    path("index/", views.CampaingsListView.as_view(), name="campaigns.list"),
    path("<int:pk>/", views.CampaignDetailView.as_view(), name="campaign.details"),
    path("create/", views.CreateCampaignFormView.as_view(), name="campaign.create"),
]
