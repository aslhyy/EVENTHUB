
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


from core.permissions import IsSponsor, IsOrganizer
from .models import Sponsor, EventSponsor
from .serializers import SponsorSerializer, EventSponsorSerializer




# =========================
# SPONSOR
# =========================
class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticated & IsSponsor]


    def get_queryset(self):
        return Sponsor.objects.all()

# =========================
# SPONSOR POR EVENTO
# =========================
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import EventSponsor
from .serializers import EventSponsorSerializer
from core.permissions import IsAdmin, IsOrganizer


class EventSponsorViewSet(ModelViewSet):
    queryset = EventSponsor.objects.all()
    serializer_class = EventSponsorSerializer
    permission_classes = [IsAuthenticated & (IsAdmin | IsOrganizer)]


    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return EventSponsor.objects.none()
        user = self.request.user
        if user.is_staff:
            return EventSponsor.objects.all()
        return EventSponsor.objects.filter(event__organizer=user)


