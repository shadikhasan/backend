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
    calculated_cost = serializers.SerializerMethodField()

    class Meta:
        model = DumpingEntryRecord
        fields = ['EntryID', 'Vehicle', 'SecondaryTransferStation', 'Landfill', 'VolumeOfWaste', 'Distance', 'calculated_cost']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            data['Vehicle'] = VehicleSerializer(instance.Vehicle).data
            data['Landfill'] = LandfillSerializer(instance.Landfill).data
            data['SecondaryTransferStation'] = SecondaryTransferStationSerializer(instance.SecondaryTransferStation).data
        return data

    def get_calculated_cost(self, obj):
        load_fraction = obj.VolumeOfWaste / obj.Vehicle.Capacity
        C_loaded = obj.Vehicle.FuelCostLoaded
        C_unloaded = obj.Vehicle.FuelCostUnloaded
        cost_per_kilometer = C_unloaded + load_fraction * (C_loaded - C_unloaded)
        total_cost = cost_per_kilometer * obj.Distance
        return round(total_cost, 3)