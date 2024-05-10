from django.http import HttpResponse
from django.contrib import admin
from .models import *
from core.models import *
#for pdf importing 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def download_pdf(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="billing_report.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('PDF Report')
    
    # Add Title
    title_text = "Billing Report"
    pdf.setFont("Helvetica-Bold", 16)  # Set font and size for title
    pdf.drawString(250, 650, title_text)  # Draw the title at specified position


    excluded_fields = ['CreatedAt', 'UpdatedAt', 'TimeOfArrival', 'TimeOfDeparture']
    headers = [field.verbose_name for field in self.model._meta.fields if field.name not in excluded_fields]
    vehicle_headers = [field.verbose_name for field in Vehicle._meta.fields if field.name not in excluded_fields]
    data = [headers]

    
    for obj in queryset:
        billing_data = [str(getattr(obj, field.name)) for field in self.model._meta.fields if field.name not in excluded_fields]
        data_row = billing_data
        data.append(data_row)
        
    data.append(vehicle_headers) 
    for obj in queryset:
        vehicle_data = [str(getattr(obj.Vehicle, field.name)) for field in Vehicle._meta.fields if field.name not in excluded_fields]
        data_row = vehicle_data

        data.append(data_row)
        data_row = data_row
        #print(data_row)
        
    
    # Calculate the total bill for the queryset
    total_bill = sum([self.calculated_cost(obj) for obj in queryset])
    # Append the "Total bill" row with the calculated total bill to the data list
    data.append([" ","Total bill (Oill allocation)"," = ", f"{total_bill} TK"])
    
    
    table = Table(data)
    # Define TableStyle to merge the last row across all columns
    table_style = TableStyle([('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                              ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
                              ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                              ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                              ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                              ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black)])
    
    # Add borders to all rows
    for i in range(len(data)):
        table_style.add('LINEABOVE', (0, i), (-1, i), 1, colors.black)
        table_style.add('LINEBELOW', (0, i), (-1, i), 1, colors.black)
        
    table.setStyle(table_style)

    canvas_width = 800
    canvas_height = 600
    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 0, canvas_height - len(data) * 20)

    pdf.save()
    return response

download_pdf.short_description = 'Download selected item as PDF.'
    
    
    


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    search_fields = ['RegistrationNumber']
    ordering = ['VehicleID']
    list_display = ['VehicleID', 'RegistrationNumber', 'Type', 'Capacity', 'FuelCostLoaded', 'FuelCostUnloaded', 'CreatedAt', 'UpdatedAt']

@admin.register(SecondaryTransferStation)
class SecondaryTransferStationAdmin(admin.ModelAdmin):
    search_fields = ['STSID']
    ordering = ['STSID']
    list_display = ['STSID', 'WardNumber', 'area', 'Location', 'Capacity', 'Latitude', 'Longitude', 'CreatedAt', 'UpdatedAt']
@admin.register(Landfill)
class LandfillAdmin(admin.ModelAdmin):
    search_fields = ['LandfillID']
    ordering = ['LandfillID']
    list_display = ['LandfillID', 'Name', 'Location', 'Capacity', 'Latitude', 'Longitude',  'CreatedAt', 'UpdatedAt']

@admin.register(WasteTransfer)
class WasteTransferAdmin(admin.ModelAdmin):
    autocomplete_fields = ['Vehicle', 'Source', 'Destination']
    ordering = ['TransferID']
    list_display = ['TransferID', 'Vehicle', 'Source', 'Destination', 'Distance', 'VolumeOfWaste', 'TimeOfArrival', 'TimeOfDeparture', 'CreatedAt', 'UpdatedAt']
    
    
@admin.register(DumpingEntryRecord)
class DumpingEntryRecordAdmin(admin.ModelAdmin):
    autocomplete_fields = ['Vehicle']
    list_display = ['EntryID', 'Vehicle', 'calculated_cost', 'SecondaryTransferStation', 'Landfill', 'VolumeOfWaste', 'TimeOfArrival', 'TimeOfDeparture', 'CreatedAt', 'UpdatedAt']

    readonly_fields = ['calculated_cost']
    actions = [download_pdf]
    
    
    def cost_per_kilometer(self, obj):
        # Assuming C_unloaded and C_loaded are defined somewhere
        # Calculate the fraction of load relative to the truck's capacity
        load_fraction = obj.VolumeOfWaste / obj.Vehicle.Capacity

        C_loaded = obj.Vehicle.FuelCostLoaded
        C_unloaded = obj.Vehicle.FuelCostUnloaded
        # Interpolate the fuel cost per kilometer based on load
        cost_per_kilometer = C_unloaded + load_fraction * (C_loaded - C_unloaded)

        return cost_per_kilometer
    
    def calculated_cost(self, obj):
        total_cost = self.cost_per_kilometer(obj) * obj.Distance
        return round(total_cost, 3)
    
    calculated_cost.short_description = "Oill Allocation (TK)"

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    ordering = ['RoleID']
    list_display = ['RoleID', 'Name', 'Description', 'CreatedAt', 'UpdatedAt']
