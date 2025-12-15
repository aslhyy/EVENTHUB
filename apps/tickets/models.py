from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings
from apps.events.models import Event, Category, Venue




class TicketType(models.Model):
    """
    Tipos de tickets para un evento (General, VIP, Early Bird, etc.)
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='ticket_types',
        verbose_name="Evento"
    )
    name = models.CharField(max_length=100, verbose_name="Nombre")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio"
    )
    quantity = models.PositiveIntegerField(verbose_name="Cantidad Disponible")
    sold_count = models.PositiveIntegerField(default=0, verbose_name="Vendidos")
    sale_start = models.DateTimeField(verbose_name="Inicio de Venta")
    sale_end = models.DateTimeField(verbose_name="Fin de Venta")


    class Meta:
        verbose_name = "Tipo de Ticket"
        verbose_name_plural = "Tipos de Tickets"
        ordering = ['price']
        unique_together = ('event', 'name')


    def __str__(self):
        return f"{self.name} - {self.event.title}"


    @property
    def available_quantity(self):
        return self.quantity - self.sold_count


    @property
    def is_available(self):
        now = timezone.now()
        return (
            self.sale_start <= now <= self.sale_end
            and self.available_quantity > 0
            and not self.event.is_past
        )


class Ticket(models.Model):
    """
    Ticket comprado por un usuario
    """
    STATUS_CHOICES = [
        ('valid', 'Válido'),
        ('used', 'Usado'),
        ('cancelled', 'Cancelado'),
    ]


    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.PROTECT,
        related_name='tickets',
        verbose_name="Tipo de Ticket"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='valid'
    )
    price_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio Pagado"
    )


    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-purchase_date']


    def __str__(self):
        return f"{self.ticket_type.name} - {self.user.username}"


    @property
    def is_valid(self):
        return (
            self.status == 'valid'
            and not self.ticket_type.event.is_past
        )


    def can_be_cancelled(self):
        return (
            self.status == 'valid'
            and timezone.now() < self.ticket_type.event.start_date
        )