import io
import uuid
import random
import string
from decimal import Decimal


from django.core.files.base import ContentFile
from django.utils.formats import number_format
from django.conf import settings


import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas




# ==========================
# CÓDIGOS
# ==========================


def generate_random_code(length=8):
    """
    Genera un código alfanumérico aleatorio.
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))




def generate_ticket_code():
    """
    Genera código único para ticket.
    """
    return f"TCK-{generate_random_code(10)}"




# ==========================
# QR
# ==========================


def generate_qr_code(data):
    """
    Genera una imagen QR y retorna ContentFile.
    """
    qr = qrcode.make(data)
    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')


    return ContentFile(
        buffer.getvalue(),
        name=f"qr_{uuid.uuid4()}.png"
    )




# ==========================
# PDF
# ==========================


def generate_ticket_pdf(ticket):
    """
    Genera PDF del ticket.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)


    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 800, "🎟️ Ticket de Evento")


    p.setFont("Helvetica", 12)
    p.drawString(50, 760, f"Evento: {ticket.ticket_type.event.title}")
    p.drawString(50, 740, f"Asistente: {ticket.user.username}")
    p.drawString(50, 720, f"Ticket ID: {ticket.id}")
    p.drawString(50, 700, f"Fecha: {ticket.ticket_type.event.start_date}")


    p.showPage()
    p.save()


    return ContentFile(
        buffer.getvalue(),
        name=f"ticket_{ticket.code}.pdf"
    )




# ==========================
# FORMATO
# ==========================


def format_currency(value, currency="COP"):
    """
    Formatea moneda correctamente.
    """
    if value is None:
        return "0"


    value = Decimal(value)
    return f"{currency} {number_format(value, 0, force_grouping=True)}"




# ==========================
# IP
# ==========================


def get_client_ip(request):
    """
    Obtiene IP real del cliente.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


