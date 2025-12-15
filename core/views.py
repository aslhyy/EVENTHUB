"""
Vistas compartidas del sistema (core)
"""

from django.http import JsonResponse
from django.db import connection
from django.utils import timezone
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from apps.events.models import Event
from apps.tickets.models import Ticket
from apps.attendees.models import Attendee

from core.permissions import IsAdmin, IsOrganizer
from core.serializers import RegisterSerializer


User = get_user_model()

# =====================================================
# Health Check (Render / Monitoring)
# =====================================================
@extend_schema(
    request=None,
    responses={
        200: {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "database": {"type": "string"},
            },
        }
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    try:
        connection.ensure_connection()
        db_status = "ok"
    except Exception:
        db_status = "error"

    return JsonResponse(
        {
            "status": "ok",
            "database": db_status,
        },
        status=200,
    )


# =====================================================
# Registro de usuarios
# =====================================================
@extend_schema(
    request=RegisterSerializer,
    responses={201: RegisterSerializer},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """
    Registro público de usuarios
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "Usuario creado correctamente",
                "user_id": user.id,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# Dashboard de estadísticas (Admin / Organizer)
# =====================================================
@extend_schema(request=None, responses=None)
@api_view(["GET"])
@permission_classes([IsAuthenticated & (IsAdmin | IsOrganizer)])
def dashboard_stats(request):
    """
    Dashboard consolidado de métricas del sistema
    """
    now = timezone.now()

    # Eventos activos
    active_events = Event.objects.filter(
        status="published",
        start_date__gte=now,
    )

    # Tickets vendidos
    tickets_qs = Ticket.objects.filter(status="valid")

    total_tickets_sold = tickets_qs.count()
    total_revenue = (
        tickets_qs.aggregate(total=Sum("price_paid"))["total"] or 0
    )

    # Asistentes únicos con check-in
    total_attendees = (
        Attendee.objects.filter(status="checked_in")
        .values("user")
        .distinct()
        .count()
    )

    # Ventas por evento
    sales_by_event = (
        tickets_qs.values("ticket_type__event__title")
        .annotate(
            tickets_sold=Count("id"),
            revenue=Sum("price_paid"),
        )
        .order_by("-revenue")
    )

    return Response(
        {
            "events_active": active_events.count(),
            "tickets_sold": total_tickets_sold,
            "total_revenue": total_revenue,
            "attendees": total_attendees,
            "sales_by_event": sales_by_event,
        }
    )


# =====================================================
# API Root
# =====================================================
@extend_schema(request=None, responses=None)
@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    """
    Punto de entrada de la API
    """
    return Response(
        {
            "message": "Bienvenido a EventHub API 🚀",
            "endpoints": {
                "health": "/health/",
                "login": "/api/auth/login/",
                "refresh": "/api/auth/refresh/",
                "register": "/api/auth/register/",
                "events": "/api/events/",
                "tickets": "/api/tickets/",
                "attendees": "/api/attendees/",
                "sponsors": "/api/sponsors/",
                "dashboard": "/api/dashboard/",
                "schema": "/api/schema/",
                "swagger": "/swagger/",
                "redoc": "/redoc/",
            },
        }
    )
