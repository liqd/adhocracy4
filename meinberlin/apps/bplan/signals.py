from django.db.models.signals import post_save
from django.dispatch import receiver

from . import emails
from . import tasks
from .models import Bplan
from .models import Statement


@receiver(post_save, sender=Bplan)
def get_location(sender, instance, update_fields, **kwargs):
    if instance.identifier and (not update_fields or
                                'point' not in update_fields):
        tasks.get_location_information(instance.pk)


@receiver(post_save, sender=Statement)
def send_notification(sender, instance, created, **kwargs):
    if created:
        emails.OfficeWorkerNotification.send(instance)

        if instance.email:
            emails.SubmitterConfirmation.send(instance)
