from django.core.mail import send_mail
from django.conf import settings


def send_appointment_email(
    patient_email,
    patient_name,
    appointment_date
):

    send_mail(

        "HomeoCare Appointment Approved",

        f"""
Hello {patient_name},

Your appointment has been approved.

Appointment Date:
{appointment_date}

Please visit HomeoCare clinic on your scheduled date.

Thank you.
HomeoCare Team
""",

        settings.EMAIL_HOST_USER,

        [patient_email],

        fail_silently=False,

    )
def send_appointment_cancelled_email(
    patient_email,
    patient_name,
    appointment_date
):

    send_mail(

        "HomeoCare Appointment Cancelled",

        f"""
Hello {patient_name},

We regret to inform you that your appointment scheduled for

{appointment_date}

has been cancelled by the receptionist.

If you would like to book another appointment, please log in to the HomeoCare portal or contact the clinic.

Thank you for your understanding.

HomeoCare Team
""",

        settings.EMAIL_HOST_USER,

        [patient_email],

        fail_silently=False,

    )