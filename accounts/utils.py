from django.core.mail import send_mail
import random
from django.conf import settings

def generate_reset_code():
    return str(random.randint(100000, 999999))

def send_reset_email(email, code):
    subject = "Parolni tiklash uchun kod"
    message = f"Assalomu alaykum,\n\nSizning parolni tiklash kodingiz: {code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
