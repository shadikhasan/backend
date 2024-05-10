# serializers.py
from rest_framework import serializers
from core.utils import aws_map_route_api
from .models import *

class WasteTransferSerializer(serializers.ModelSerializer):
    ShortestRoute = serializers.SerializerMethodField()
    FastestRoute = serializers.SerializerMethodField()

    class Meta:
        model = WasteTransfer
        fields = ['Vehicle', 'Source', 'Destination', 'Distance', 'VolumeOfWaste', 'TimeOfArrival', 'TimeOfDeparture', 'ShortestRoute', 'FastestRoute']

    def get_ShortestRoute(self, obj):
        source = obj.Source
        destination = obj.Destination
        shortest_route = aws_map_route_api(source.Latitude, source.Longitude, destination.Latitude, destination.Longitude, 'ShortestRoute')
        return shortest_route

    def get_FastestRoute(self, obj):
        source = obj.Source
        destination = obj.Destination
        fastest_route = aws_map_route_api(source.Latitude, source.Longitude, destination.Latitude, destination.Longitude, 'FastestRoute')
        return fastest_route

class SecondaryTransferStationSerializer(serializers.ModelSerializer):
    http_method_names = ['get'] 
    class Meta:
        model = SecondaryTransferStation
        fields = '__all__'

class LandfillSerializer(serializers.ModelSerializer):
    http_method_names = ['get'] 
    class Meta:
        model = Landfill
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    http_method_names = ['get'] 
    class Meta:
        model = Vehicle
        fields = '__all__'