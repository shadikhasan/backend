from django.db import models
from core.models import CustomUser
from django.utils import timezone
from django.db.models.signals import post_save
from managers.models import STSManager
from waste_management.models import *
import logging
class IssueReport(models.Model):
    location = models.CharField(max_length=255)
    issue_type = models.CharField(max_length=100)
    description = models.TextField()
    sts = models.ForeignKey(SecondaryTransferStation, on_delete=models.CASCADE, default=1)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Issue Report - {self.pk}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use CustomUser here
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.message}'

logger = logging.getLogger(__name__)

@receiver(post_save, sender=IssueReport)
def create_notification(sender, instance, created, **kwargs):
    if created:
        sts_manager = STSManager.objects.filter(sts=instance.sts).first()
        if sts_manager:
            try:
                Notification.objects.create(
                    user=sts_manager.user,
                    message=f'New Issue Report Created - ID: {instance.pk}, Location: {instance.location}, Issue Type: {instance.issue_type}'
                )
                logger.info("Notification created successfully.")
            except Exception as e:
                logger.error(f"Error creating notification: {e}")
        else:
            logger.warning("STS Manager not found for the given SecondaryTransferStation.")
    else:
        logger.info("IssueReport instance not created. No notification generated.")
        
        
        
class PublicNotification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
    
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class VolunteerRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='volunteer_registrations')
    registration_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.volunteer.username} registered for {self.event.name}"


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name