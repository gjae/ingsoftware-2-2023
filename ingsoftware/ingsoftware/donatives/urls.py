from django.urls import path


from ingsoftware.donatives import views

urlpatterns = [
    path("<int:pk>/", views.DonativeCreateView.as_view(), name="campaigns.donatives.donate"),
]
