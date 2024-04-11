from django.contrib import admin
from .models import Campaign

# Register your models here.

@admin.register(Campaign)
class CampaignModelAdmin(admin.ModelAdmin):
    pass
