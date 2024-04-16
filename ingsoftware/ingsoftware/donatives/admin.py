from django.contrib import admin

from .models import Donation
# Register your models here.

@admin.register(Donation)
class DonationAdminModel(admin.ModelAdmin):
    pass