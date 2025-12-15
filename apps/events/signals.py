# apps/events/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.events.models import Event
from core.emails import EmailService




@receiver(post_save, sender=Event)
def event_status_change(sender, instance, **kwargs):
    if instance.status == "cancelled":
        EmailService.send_event_cancelled(instance)