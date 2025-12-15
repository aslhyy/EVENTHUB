# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from apps.events.models import Event, Category, Venue
from .models import TicketType, Ticket




class TicketAPITest(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )


        category = Category.objects.create(name="Conciertos")
        venue = Venue.objects.create(
            name="Teatro",
            address="Calle 1",
            city="Bogotá",
            state="Cundinamarca",
            capacity=1000
        )


        self.event = Event.objects.create(
            title="Evento Test",
            description="Descripción",
            category=category,
            venue=venue,
            organizer=self.user,
            start_date=timezone.now() + timedelta(days=10),
            end_date=timezone.now() + timedelta(days=10, hours=3),
            capacity=500,
            status='published'
        )


        self.ticket_type = TicketType.objects.create(
            event=self.event,
            name="General",
            price=50000,
            quantity=100,
            sale_start=timezone.now() - timedelta(days=1),
            sale_end=timezone.now() + timedelta(days=5)
        )


    def test_list_ticket_types(self):
        response = self.client.get('/api/ticket-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_buy_ticket_unauthorized(self):
        response = self.client.post('/api/tickets/', {
            'ticket_type': self.ticket_type.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_buy_ticket_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/tickets/', {
            'ticket_type': self.ticket_type.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_cancel_ticket(self):
        self.client.force_authenticate(user=self.user)
        ticket = Ticket.objects.create(
            ticket_type=self.ticket_type,
            user=self.user,
            price_paid=self.ticket_type.price
        )


        response = self.client.post(f'/api/tickets/{ticket.id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
