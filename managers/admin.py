from django.contrib import admin
from .models import STSManager, LandfillManager

@admin.register(STSManager)
class STSManagerAdmin(admin.ModelAdmin):
    fields = ['user', 'sts']

@admin.register(LandfillManager)
class LandfillManagerAdmin(admin.ModelAdmin):
    fields = ['user', 'landfill']
