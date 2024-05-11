from rest_framework import serializers
from .models import STSManager, LandfillManager, ContractorManager
from user_management.serializers import *
class STSManagerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = STSManager
        fields = ['id', 'user', 'sts']

class LandfillManagerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = LandfillManager
        fields = ['id', 'user', 'landfill']

class ContractorManagerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = ContractorManager
        fields = ['id', 'user', 'contact_number', 'assigned_contractor_company', 'access_level']
