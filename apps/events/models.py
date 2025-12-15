
from django.db import models
from django.conf import settings


# Create your models here.
"""
Modelos para la gestión de eventos.
"""
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.timezone import now

class Category(models.Model):
    """
    Categorías de eventos (Concierto, Conferencia, Deportes, etc.)
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icono")


    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']


    def __str__(self):
        return self.name


    @property
    def events_count(self):
        """Retorna el número de eventos en esta categoría."""
        return self.events.filter(status='published').count()




class Venue(models.Model):
    """
    Lugares donde se realizan los eventos.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    address = models.CharField(max_length=300, verbose_name="Dirección")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    state = models.CharField(max_length=100, verbose_name="Departamento/Estado")
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Capacidad"
    )
   
    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
        ordering = ['name']


    def __str__(self):
        return f"{self.name} - {self.city}"


    @property
    def full_address(self):
        """Retorna la dirección completa."""
        return f"{self.address}, {self.city}, {self.state}"




class Event(models.Model):
    """
    Modelo principal de eventos.
    """
    STATUS_CHOICES = [
        ('published', 'Publicado'),
        ('ongoing', 'En Curso'),
        ('finished', 'Finalizado'),
        ('cancelled', 'Cancelado'),
    ]


    # Información básica
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Descripción")


    # Relaciones


    # Este refiere a la categoría del evento
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='events',
        verbose_name="Categoría"
    )


    # Este refiere al lugar del evento
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        verbose_name="Lugar"
    )


    # Este refiere al organizador del evento
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
   
    # Fechas y horarios
    start_date = models.DateTimeField(verbose_name="Fecha de Inicio")
    end_date = models.DateTimeField(verbose_name="Fecha de Fin")
   
    # Configuración


    # Estado del evento
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='published',
        verbose_name="Publicado"
    )


    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Capacidad"
    )
    is_free = models.BooleanField(default=False, verbose_name="¿Es Gratuito?")
    is_online = models.BooleanField(default=False, verbose_name="¿Es Virtual?")
    online_url = models.URLField(
        blank=True,
        verbose_name="URL del Evento Virtual"
    )
   
    # Class meta es para definir metadatos del modelo
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['slug']),
        ]


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        """Override save para generar slug automáticamente."""
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
           
            # Asegurar que el slug es único
            original_slug = self.slug
            counter = 1
            while Event.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
       
        super().save(*args, **kwargs)


    @property
    def is_active(self):
        return self.start_date > now()

    @property
    def is_past(self):
        if not self.end_date:
            return False
        return self.end_date < timezone.now()


    @property
    def tickets_sold(self):
        """Retorna el número de tickets vendidos."""
        return self.ticket_types.aggregate(
            total=models.Sum('sold_count')
        )['total'] or 0


    @property
    def tickets_available(self):
        """Retorna el número de tickets disponibles."""
        return self.capacity - self.tickets_sold


    @property
    def is_sold_out(self):
        """Verifica si el evento está agotado."""
        return self.tickets_sold >= self.capacity