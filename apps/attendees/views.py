from django.db import models  # <-- Agregar esta línea
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from core.permissions import IsAdmin, IsOrganizer
from .models import Attendee
from .serializers import AttendeeSerializer


class AttendeeViewSet(ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        attendee, created = Attendee.objects.get_or_create(
            event_id=request.data.get("event"),
            user=request.user,
            defaults={
                "ticket_id": request.data.get("ticket")
            },
        )

        serializer = self.get_serializer(attendee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Attendee.objects.none()

        user = self.request.user

        if user.is_staff:
            return Attendee.objects.all()

        return Attendee.objects.filter(
            models.Q(user=user) |
            models.Q(event__organizer=user)
        )

    def perform_create(self, serializer):
        event = serializer.validated_data["event"]

        # Evita violar UNIQUE(event, user)
        if Attendee.objects.filter(
            event=event,
            user=self.request.user
        ).exists():
            raise ValidationError(
                {"detail": "User already registered for this event"}
            )

        serializer.save(user=self.request.user)

    # =========================
    # CHECK-IN
    # =========================
    @extend_schema(request=None, responses={200: None})
    @action(detail=True, methods=["post"])
    def check_in(self, request, pk=None):
        attendee = Attendee.objects.get(pk=pk)

        if attendee.checked_in:
            return Response(
                {"detail": "El asistente ya hizo check-in"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        attendee.checked_in = True
        attendee.save()

        return Response(
            {"detail": "Check-in exitoso"},
            status=status.HTTP_200_OK
        )
