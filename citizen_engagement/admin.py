from django.contrib import admin
from .models import *

@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ('location', 'issue_type', 'sts', 'description', 'anonymous', 'created_at')
    search_fields = ['location', 'issue_type', 'description']
    list_filter = ['anonymous', 'created_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')

@admin.register(PublicNotification)
class PublicNotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')