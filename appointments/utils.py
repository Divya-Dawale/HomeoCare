from datetime import datetime, timedelta
from .models import Appointment
from doctors.models import DoctorSettings


def get_next_appointment_no(appointment_date):
    last_appointment = (
        Appointment.objects
        .filter(
            appointment_date=appointment_date,
            appointment_no__isnull=False
        )
        .order_by("-appointment_no")
        .first()
    )

    if last_appointment:
        return last_appointment.appointment_no + 1

    return 1


def get_appointment_time(appointment_date, appointment_no):
    doctor_settings = DoctorSettings.objects.first()

    if not doctor_settings:
        return None

    if not doctor_settings.opening_time:
        return None

    duration = doctor_settings.appointment_duration

    opening_datetime = datetime.combine(
        appointment_date,
        doctor_settings.opening_time
    )

    appointment_datetime = (
        opening_datetime
        + timedelta(
            minutes=(appointment_no - 1) * duration
        )
    )

    return appointment_datetime.time()