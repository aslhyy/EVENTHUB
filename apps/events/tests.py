from django.test import TestCase


# Create your tests here.
"""
Tests para eventos.
"""
from datetime import timedelta


from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone


from rest_framework.test import APITestCase
from rest_framework import status


from .models import Category, Venue, Event




# =========================
# MODELS
# =========================
class CategoryModelTest(TestCase):
    """Tests para el modelo Category."""


    def setUp(self):
        self.category = Category.objects.create(
            name="Conciertos",
            description="Eventos musicales"
        )


    def test_category_creation(self):
        self.assertEqual(self.category.name, "Conciertos")
        self.assertEqual(str(self.category), "Conciertos")


    def test_events_count(self):
        self.assertEqual(self.category.events_count, 0)




class VenueModelTest(TestCase):
    """Tests para el modelo Venue."""


    def setUp(self):
        self.venue = Venue.objects.create(
            name="Teatro Colón",
            address="Calle 10 # 5-32",
            city="Bogotá",
            state="Cundinamarca",
            capacity=1500
        )


    def test_venue_creation(self):
        self.assertEqual(self.venue.name, "Teatro Colón")
        self.assertEqual(self.venue.capacity, 1500)
        self.assertIn("Bogotá", str(self.venue))


    def test_full_address(self):
        expected_address = "Calle 10 # 5-32, Bogotá, Cundinamarca"
        self.assertEqual(self.venue.full_address, expected_address)




class EventModelTest(TestCase):
    """Tests para el modelo Event."""


    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )


        self.category = Category.objects.create(
            name="Conciertos"
        )


        self.venue = Venue.objects.create(
            name="Test Venue",
            address="Test Address",
            city="Test City",
            state="Test State",
            capacity=1000
        )


        self.event = Event.objects.create(
            title="Concierto de Rock",
            description="Gran concierto de rock",
            category=self.category,
            venue=self.venue,
            organizer=self.user,
            start_date=timezone.now() + timedelta(days=30),
            end_date=timezone.now() + timedelta(days=30, hours=3),
            capacity=500,
            status='published'
        )


    def test_event_creation(self):
        self.assertEqual(self.event.title, "Concierto de Rock")
        self.assertEqual(self.event.capacity, 500)


    def test_slug_generation(self):
        self.assertIsNotNone(self.event.slug)
        self.assertIn("concierto", self.event.slug)


    def test_is_active(self):
        self.assertTrue(self.event.is_active)


    def test_tickets_available(self):
        self.assertEqual(self.event.tickets_available, 500)




# =========================
# API
# =========================
class EventAPITest(APITestCase):
    """Tests para la API de eventos."""


    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )


        self.category = Category.objects.create(
            name="Conciertos"
        )


        self.venue = Venue.objects.create(
            name="Test Venue",
            address="Test Address",
            city="Test City",
            state="Test State",
            capacity=1000
        )


    def test_list_events(self):
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_event_unauthorized(self):
        """
        Test que verifica que un usuario NO autenticado no puede crear eventos.
        DRF con IsAuthenticated devuelve 401 cuando el usuario es None (AnonymousUser).
        """
        data = {
            'title': 'Nuevo Evento',
            'description': 'Descripción',
            'category': self.category.id,
            'venue': self.venue.id,
            'start_date': (timezone.now() + timedelta(days=30)).isoformat(),
            'end_date': (timezone.now() + timedelta(days=30, hours=3)).isoformat(),
            'capacity': 100
        }

        response = self.client.post('/api/events/', data, format='json')
        
        # 🔥 DEBE devolver 401 cuando no hay autenticación
        self.assertIn(
            response.status_code, 
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )


    def test_create_event_authorized(self):
        """
        Test que verifica que un usuario autenticado SÍ puede crear eventos.
        """
        self.client.force_authenticate(user=self.user)


        data = {
            'title': 'Nuevo Evento',
            'description': 'Descripción del evento',
            'category': self.category.id,
            'venue': self.venue.id,
            'start_date': (timezone.now() + timedelta(days=30)).isoformat(),
            'end_date': (timezone.now() + timedelta(days=30, hours=3)).isoformat(),
            'capacity': 100,
            'status': 'published'
        }


        response = self.client.post('/api/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el organizador fue asignado correctamente
        self.assertEqual(response.data['organizer'], self.user.id)