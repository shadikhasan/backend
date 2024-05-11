# serializers.py
from rest_framework import serializers
from .models import *

class ThirdPartyContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThirdPartyContractor
        fields = '__all__'


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'