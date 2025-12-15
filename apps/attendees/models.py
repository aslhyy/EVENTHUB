from django.db import models
from django.utils import timezone
from apps.tickets.models import Ticket
from django.conf import settings
from apps.events.models import Event, Category, Venue
from django.contrib.auth import get_user_model
User = get_user_model()


class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
    checked_in = models.BooleanField(default=False)

    def check_in(self):
        if self.checked_in:
            raise ValueError("El asistente ya hizo check-in")
        self.checked_in = True
        self.save()
    """
    Asistentes a eventos (check-in).
    """
    STATUS_CHOICES = [
        ('registered', 'Registrado'),
        ('checked_in', 'Asistió'),
        ('no_show', 'No asistió'),
    ]


    id = models.AutoField(primary_key=True)


    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='attendees'
    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendances'
    )


    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name='attendee'
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='registered'
    )


    check_in_time = models.DateTimeField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=["event", "user"],
                    name="unique_attendee_per_event"
                )
            ]


    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


    def check_in(self):
        """
        Marca asistencia si el ticket es válido
        y el evento está en curso.
        """
        now = timezone.now()


        if not self.ticket.is_valid:
            raise ValueError("Ticket inválido")


        if not (self.event.start_date <= now <= self.event.end_date):
            raise ValueError("El evento no está en curso")


        self.status = 'checked_in'
        self.check_in_time = now
        self.save()
