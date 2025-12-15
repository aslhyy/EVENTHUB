from rest_framework.routers import DefaultRouter
from .views import TicketTypeViewSet, TicketViewSet

router = DefaultRouter()  # 👈 SLASH FINAL ACTIVADO

router.register(r"ticket-types", TicketTypeViewSet)
router.register(r"tickets", TicketViewSet)

urlpatterns = router.urls
