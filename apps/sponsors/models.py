from django.db import models
from django.utils import timezone
from apps.events.models import Event

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="sponsors/", blank=True, null=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class EventSponsor(models.Model):
    LEVEL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_sponsors"
    )
    sponsor = models.ForeignKey(
        Sponsor,
        on_delete=models.CASCADE,
        related_name="sponsored_events"
    )


    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES
    )


    contribution_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("event", "sponsor")


    def __str__(self):
        return f"{self.sponsor} → {self.event} ({self.level})"


    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date


    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days

