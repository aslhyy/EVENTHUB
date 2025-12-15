from django.core.mail import send_mail
from django.conf import settings




class EmailService:
    """
    Servicio centralizado de emails.
    """


    @staticmethod
    def send_ticket_purchase_confirmation(ticket):
        subject = f"🎟️ Confirmación de compra - {ticket.ticket_type.event.title}"


        message = (
            f"Hola {ticket.user.username},\n\n"
            "Tu ticket ha sido confirmado exitosamente.\n\n"
            f"Evento: {ticket.ticket_type.event.title}\n"
            f"Fecha: {ticket.ticket_type.event.start_date}\n"
            f"Tipo de ticket: {ticket.ticket_type.name}\n"
            f"Precio pagado: ${ticket.price_paid}\n\n"
            "¡Te esperamos!"
        )


        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [ticket.user.email],
            fail_silently=True
        )


    @staticmethod
    def send_check_in_confirmation(attendee):
        subject = "✅ Check-in confirmado"
        message = (
            f"Hola {attendee.user.username},\n\n"
            f"Tu ingreso al evento {attendee.event.title} ha sido registrado.\n"
            "¡Disfruta el evento!"
        )


        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [attendee.user.email],
            fail_silently=True
        )