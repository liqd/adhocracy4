from allauth.account.signals import email_confirmed
from django.dispatch import receiver

from . import emails


@receiver(email_confirmed)
def send_welcome_email(request, email_address, **kwargs):
    user = email_address.user
    emails.WelcomeEmail.send(user)
