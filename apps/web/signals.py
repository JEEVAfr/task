from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.dispatch import receiver
from .models import *
import os

@receiver(post_save, sender=PersonalDetails)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        # Create notification message
        message = f"New User {instance.first_name} has been created."
        Notification.objects.create(message=message)

        # Assuming the PDF is stored in the 'Downloads' folder
        pdf_path = '/Users/jeevas/Downloads/offerletter.pdf'

        # Create the email message
        email = EmailMessage(
            subject='New User Registration',
            body=message,
            from_email='jeevakumar1831@gmail.com',
            to=[instance.email_id],
            cc= ['waterbottle@malinator.com'],
            bcc = ['waterbottle@malinator.com']
        )

        # Open the PDF file and read it in binary mode
        with open(pdf_path, 'rb') as file:
            pdf_data = file.read()

            # Attach the PDF to the email
            email.attach('offerletter.pdf', pdf_data, 'application/pdf')

        # Send the email
        email.send(fail_silently=False)

        print(message)
