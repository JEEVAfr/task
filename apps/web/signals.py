from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

# if user is created it will send the notification
@receiver(post_save, sender=PersonalDetails)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        message = f"New User {instance.first_name} has been created."  
        Notification.objects.create(message=message)
        print(message)
