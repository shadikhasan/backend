# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from waste_management.models import *
from core.models import *
from django.db import models
from rest_framework import status
import requests
import json
from core.utils import aws_map_route_api

class Last7DaysDumpingRecords(generics.ListAPIView):
    serializer_class = DumpingEntryRecordSerializer
    #permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Calculate the date 7 days ago from today
        last_week = datetime.now() - timedelta(days=7)
        # Filter records for the last 7 days
        queryset = DumpingEntryRecord.objects.filter(TimeOfArrival__gte=last_week)
        return queryset

class TotalDumpingRecords(generics.ListAPIView):
    serializer_class = DumpingEntryRecordSerializer

    def get_queryset(self):
        # Get total dumping records
        queryset = DumpingEntryRecord.objects.all()
        return queryset


class VehicleSummary(APIView):
    def get(self, request):
        # Get total count of vehicles
        total_vehicles = Vehicle.objects.count()

        # Get count of vehicles by type
        vehicles_by_type = Vehicle.objects.values('Type').annotate(count=models.Count('Type'))

        # Calculate total fuel cost for loaded and unloaded vehicles
        total_fuel_cost_loaded = Vehicle.objects.aggregate(total=models.Sum('FuelCostLoaded'))['total'] or 0
        total_fuel_cost_unloaded = Vehicle.objects.aggregate(total=models.Sum('FuelCostUnloaded'))['total'] or 0

        # Calculate average fuel cost per vehicle
        if total_vehicles > 0:
            average_fuel_cost_loaded = total_fuel_cost_loaded / total_vehicles
            average_fuel_cost_unloaded = total_fuel_cost_unloaded / total_vehicles
        else:
            average_fuel_cost_loaded = 0
            average_fuel_cost_unloaded = 0

        # Construct the summary response
        summary_data = {
            'total_vehicles': total_vehicles,
            'vehicles_by_type': vehicles_by_type,
            'total_fuel_cost_loaded': total_fuel_cost_loaded,
            'total_fuel_cost_unloaded': total_fuel_cost_unloaded,
            'average_fuel_cost_loaded': average_fuel_cost_loaded,
            'average_fuel_cost_unloaded': average_fuel_cost_unloaded
        }

        return Response(summary_data)
    
class UserSummary(APIView):
    def get(self, request):
        # Get total count of users
        total_users = CustomUser.objects.count()

        # Get count of users by role
        users_by_role = CustomUser.objects.values('role__Name').annotate(count=models.Count('role__Name'))

        # Construct the summary response
        summary_data = {
            'total_users': total_users,
            'users_by_role': users_by_role,
        }

        return Response(summary_data)
    
class LandfillWasteCapacity(APIView):
    def get(self, request):
        # Calculate total waste capacity of all landfills
        total_waste_capacity = Landfill.objects.aggregate(total_capacity=models.Sum('Capacity'))['total_capacity'] or 0

        # Construct the summary response
        summary_data = {
            'total_waste_capacity': total_waste_capacity,
        }

        return Response(summary_data)
    
    
class RouteAPIView(APIView):
    def post(self, request):
        data = request.data
        source_lat = data.get('source_lat')
        source_lon = data.get('source_lon')
        dest_lat = data.get('dest_lat')
        dest_lon = data.get('dest_lon')
        optimize_for = data.get('optimize_for')
        
        if None in [source_lat, source_lon, dest_lat, dest_lon, optimize_for]:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)
        
        result = aws_map_route_api(source_lat, source_lon, dest_lat, dest_lon, optimize_for)
        return Response(result)

    def get(self, request):
        return Response({"error": "Only POST requests are allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
