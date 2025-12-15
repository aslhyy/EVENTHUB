from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


from apps.tickets.models import Ticket
from apps.attendees.models import Attendee
from core.emails import EmailService




@receiver(post_save, sender=Ticket)
def ticket_purchased(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta cuando se compra un ticket.
    """
    if not created:
        return


    ticket = instance
    ticket_type = ticket.ticket_type
    event = ticket_type.event


    with transaction.atomic():
        # 1️⃣ Incrementar sold_count
        ticket_type.sold_count += 1
        ticket_type.save(update_fields=["sold_count"])


        # 2️⃣ Crear attendee
        Attendee.objects.create(
            event=event,
            user=ticket.user,
            ticket=ticket
        )


    # 3️⃣ Enviar email de confirmación
    EmailService.send_ticket_purchase_confirmation(ticket)