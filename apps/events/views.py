from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Event, Category, Venue
from .serializers import EventSerializer, CategorySerializer, VenueSerializer


# =========================
# CATEGORÍAS
# =========================
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# =========================
# LUGARES
# =========================
class VenueViewSet(ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticated]


# =========================
# EVENTOS
# =========================
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # 🔥 Por defecto permite todo

    def get_permissions(self):
        """
        Permisos personalizados:
        - list, retrieve: Cualquiera puede ver
        - create, update, delete: Solo autenticados
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Asigna el usuario autenticado como organizador"""
        serializer.save(organizer=self.request.user)