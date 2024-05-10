# serializers.py
from rest_framework import serializers
from .models import ThirdPartyContractor

class ThirdPartyContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThirdPartyContractor
        fields = '__all__'
