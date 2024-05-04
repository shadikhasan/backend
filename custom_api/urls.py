# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('last-7-days-dumping-records/', Last7DaysDumpingRecords.as_view(), name='last_7_days_dumping_records'),
    path('total-dumping-records/', TotalDumpingRecords.as_view(), name='total_dumping_records'),
    path('vehicle-summary/', VehicleSummary.as_view(), name='vehicle_summary'),
    path('user-summary/', UserSummary.as_view(), name='user_summary'),
    path('landfill-waste-capacity/', LandfillWasteCapacity.as_view(), name='landfill_waste_capacity'),
    path('route/', RouteAPIView.as_view(), name='route'),
    # path('route/', route_form_view, name='route'),
]
