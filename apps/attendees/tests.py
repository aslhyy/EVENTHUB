# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from apps.events.models import Event, Category, Venue
from apps.tickets.models import TicketType, Ticket
from .models import Attendee




class AttendeeAPITest(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )


        category = Category.objects.create(name="Conferencias")
        venue = Venue.objects.create(
            name="Auditorio",
            address="Calle 2",
            city="Bogotá",
            state="Cundinamarca",
            capacity=500
        )


        self.event = Event.objects.create(
            title="Evento Asistencia",
            description="Evento test",
            category=category,
            venue=venue,
            organizer=self.user,
            start_date=timezone.now() + timedelta(hours=1),
            end_date=timezone.now() + timedelta(hours=3),
            capacity=100,
            status='published'
        )


        ticket_type = TicketType.objects.create(
            event=self.event,
            name="VIP",
            price=100000,
            quantity=50,
            sale_start=timezone.now() - timedelta(days=1),
            sale_end=timezone.now() + timedelta(days=1)
        )


        self.ticket = Ticket.objects.create(
            ticket_type=ticket_type,
            user=self.user,
            price_paid=100000
        )


    def test_register_attendee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/attendees/', {
            'event': self.event.id,
            'ticket': self.ticket.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_check_in(self):
        attendee, _ = Attendee.objects.get_or_create(
            event=self.event,
            user=self.user,
            defaults={"ticket": self.ticket}
        )



        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/attendees/{attendee.id}/check_in/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
