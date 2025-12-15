from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sponsor

@receiver(post_save, sender=Sponsor)
def sponsor_created(sender, instance, created, **kwargs):
    if created:
        pass
