from rest_framework.routers import DefaultRouter
from .views import SponsorViewSet, EventSponsorViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"", SponsorViewSet, basename="sponsor")
router.register(r"event-sponsors", EventSponsorViewSet, basename="event-sponsor")

urlpatterns = router.urls


