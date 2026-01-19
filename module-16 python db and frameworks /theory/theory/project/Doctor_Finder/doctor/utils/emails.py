from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_appointment_email(subject, text_message, recipient_list, html_message=None):
    """
    Sends appointment-related emails (confirmation, approval, rejection).
    """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )

    if html_message:
        email.attach_alternative(html_message, "text/html")

    email.send(fail_silently=False)
