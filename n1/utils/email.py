from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(to_email):
    send_mail(
        subject="Welcome ",
        message="Thanks for joining!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )
