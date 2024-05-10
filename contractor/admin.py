from django.contrib import admin
from .models import *

@admin.register(ThirdPartyContractor)
class ThirdPartyContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contract_id', 'reg_id', 'reg_date', 'tin', 'contact_number', 'workforce_size', 'payment_per_ton', 'waste_per_day', 'contract_duration', 'area_of_collection', 'designated_sts']
    search_fields = ['name', 'contract_id', 'reg_id', 'area_of_collection__zone', 'designated_sts__zone']  # Add search fields for related fields
    
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'date_of_birth', 'date_of_hire', 'job_title', 'payment_rate_per_hour', 'contact_information', 'assigned_collection_route']

@admin.register(LoggedWorkingHours)
class LoggedWorkingHoursAdmin(admin.ModelAdmin):
    list_display = ['employee', 'login_time', 'logout_time', 'total_hours_worked', 'overtime_hours', 'absences_and_leaves']

@admin.register(WasteCollection)
class WasteCollectionAdmin(admin.ModelAdmin):
    list_display = ['datetime_of_collection', 'waste_amount_kg', 'contractor', 'waste_type', 'designated_sts', 'vehicle_used']
    
    
@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    readonly_fields = ['deficit', 'basic_pay', 'total_bill']
    list_display = ('contractor', 'date', 'basic_pay', 'deficit', 'fine', 'total_bill', 'collected_waste')
    search_fields = ('contractor__name', 'date')