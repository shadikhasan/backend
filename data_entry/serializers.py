# serializers.py
from rest_framework import serializers
from waste_management.models import SecondaryTransferStation, Landfill, Vehicle, WasteTransfer, DumpingEntryRecord

class SecondaryTransferStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryTransferStation
        fields = '__all__'

class LandfillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landfill
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class WasteTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTransfer
        fields = '__all__'

class DumpingEntryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DumpingEntryRecord
        fields = '__all__'
