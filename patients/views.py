from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from appointments.models import Appointment
from billing.models import Bill
from prescriptions.models import Prescription
from patients.models import Patient
from django.db import models
from django.db.models import Sum

@login_required
def patient_dashboard(request):
    patient = request.user.patient

    appointments = Appointment.objects.filter(patient=patient)

    total_appointments = appointments.count()

    completed_appointments = appointments.filter(
        status="completed"
    ).count()

    cancelled_appointments = appointments.filter(
        status="cancelled"
    ).count()

    total_bill = Bill.objects.filter(
        patient=patient,
        payment_status="paid"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    upcoming_appointments = appointments.filter(
        status__in=["approved", "waiting"]
    ).order_by("appointment_date")

    context = {
        "patient": patient,
        "total_appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "cancelled_appointments": cancelled_appointments,
        "total_bill": total_bill,
        "upcoming_appointments": upcoming_appointments,
    }

    return render(
        request,
        "patients/dashboard.html",
        context
    )

from appointments.models import Appointment

@login_required
def patient_appointments(request):

    patient = request.user.patient

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-appointment_date")

    return render(
        request,
        "patients/appointments.html",
        {
            "patient": patient,
            "appointments": appointments,
        },
    )