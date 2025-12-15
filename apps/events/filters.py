"""
Filtros para eventos.
"""
from django_filters import rest_framework as filters
from .models import Event




class EventFilter(filters.FilterSet):
    """
    Filtros avanzados para eventos.
    """


    # =========================
    # BÚSQUEDA TEXTUAL
    # =========================
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains'
    )


    description = filters.CharFilter(
        field_name='description',
        lookup_expr='icontains'
    )


    # =========================
    # CATEGORÍA
    # =========================
    category = filters.NumberFilter(
        field_name='category__id'
    )


    category_name = filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains'
    )


    # =========================
    # LUGAR
    # =========================
    venue = filters.NumberFilter(
        field_name='venue__id'
    )


    city = filters.CharFilter(
        field_name='venue__city',
        lookup_expr='icontains'
    )


    state = filters.CharFilter(
        field_name='venue__state',
        lookup_expr='icontains'
    )


    # =========================
    # ESTADO Y TIPO
    # =========================
    status = filters.ChoiceFilter(
        choices=Event.STATUS_CHOICES
    )


    is_free = filters.BooleanFilter()
    is_online = filters.BooleanFilter()


    # =========================
    # FECHAS
    # =========================
    start_date = filters.DateFilter(
        field_name='start_date',
        lookup_expr='date'
    )


    start_date_gte = filters.DateTimeFilter(
        field_name='start_date',
        lookup_expr='gte'
    )


    start_date_lte = filters.DateTimeFilter(
        field_name='start_date',
        lookup_expr='lte'
    )


    end_date = filters.DateFilter(
        field_name='end_date',
        lookup_expr='date'
    )


    end_date_gte = filters.DateTimeFilter(
        field_name='end_date',
        lookup_expr='gte'
    )


    end_date_lte = filters.DateTimeFilter(
        field_name='end_date',
        lookup_expr='lte'
    )


    # =========================
    # CAPACIDAD
    # =========================
    capacity_gte = filters.NumberFilter(
        field_name='capacity',
        lookup_expr='gte'
    )


    capacity_lte = filters.NumberFilter(
        field_name='capacity',
        lookup_expr='lte'
    )


    # =========================
    # ORGANIZADOR
    # =========================
    organizer = filters.NumberFilter(
        field_name='organizer__id'
    )


    organizer_username = filters.CharFilter(
        field_name='organizer__username',
        lookup_expr='icontains'
    )


    class Meta:
        model = Event
        fields = [
            # Texto
            'title',
            'description',


            # Categoría
            'category',
            'category_name',


            # Lugar
            'venue',
            'city',
            'state',


            # Estado
            'status',
            'is_free',
            'is_online',


            # Fechas
            'start_date',
            'start_date_gte',
            'start_date_lte',
            'end_date',
            'end_date_gte',
            'end_date_lte',


            # Capacidad
            'capacity_gte',
            'capacity_lte',


            # Organizador
            'organizer',
            'organizer_username',
        ]


