from rest_framework.routers import DefaultRouter
from .views import AttendeeViewSet

router = DefaultRouter()
router.register(r'attendees', AttendeeViewSet, basename='attendee')

urlpatterns = router.urls
