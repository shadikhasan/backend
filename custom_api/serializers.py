# serializers.py
from rest_framework import serializers
from featurs.models import DumpingEntryRecord

class DumpingEntryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DumpingEntryRecord
        fields = '__all__'