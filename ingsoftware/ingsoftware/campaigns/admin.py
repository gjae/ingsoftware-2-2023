from django.contrib import admin
from .models import Campaign, Beneficiary, Category

# Register your models here.

@admin.register(Campaign)
class CampaignModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Beneficiary)
class BeneficiaryModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass