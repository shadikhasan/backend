from django.contrib import admin
from .models import ThirdPartyContractor

@admin.register(ThirdPartyContractor)
class ThirdPartyContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contract_id', 'reg_id', 'reg_date', 'tin', 'contact_number', 'workforce_size', 'payment_per_ton', 'waste_per_day', 'contract_duration', 'area_of_collection', 'designated_sts']
    search_fields = ['name', 'contract_id', 'reg_id', 'area_of_collection__zone', 'designated_sts__zone']  # Add search fields for related fields