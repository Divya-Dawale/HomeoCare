from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from appointments.models import Appointment
from billing.models import Bill
from prescriptions.models import Prescription
from patients.models import Patient
from django.db import models
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from doctors.models import MedicalRecord
from prescriptions.models import Prescription
from patients.models import Patient
from django.db import models
from .forms import PatientForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import MedicalHistory
from .forms import MedicalHistoryForm
from django.shortcuts import get_object_or_404, redirect, render
from notifications.models import Notification
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from django.utils import timezone


@login_required
def patient_chatbot_appointment(request):

    patient = request.user.patient

    appointments = Appointment.objects.filter(
        patient=patient
    )

    today = timezone.localdate()

    upcoming = appointments.filter(
        appointment_date__gte=today,
        status__in=[
            "pending",
            "approved",
            "waiting",
            "consulting"
        ]
    ).order_by(
        "appointment_date",
        "appointment_time"
    ).first()

    latest = appointments.order_by(
        "-appointment_date",
        "-appointment_time"
    ).first()

    def appointment_data(appointment):

        if not appointment:
            return None

        return {
            "appointment_no": appointment.appointment_no,
            "date": appointment.appointment_date.strftime(
                "%d %B %Y"
            ),
            "time": (
                appointment.appointment_time.strftime("%I:%M %p")
                if appointment.appointment_time
                else "Time not specified"
            ),
            "reason": appointment.reason_for_visit,
            "status": appointment.get_status_display(),
        }

    return JsonResponse({
        "upcoming": appointment_data(upcoming),
        "latest": appointment_data(latest),
    })


@login_required
def patient_chatbot_medical_records(request):

    patient = request.user.patient

    records = MedicalRecord.objects.filter(
        patient=patient
    ).order_by("-created_at")

    latest = records.first()

    if not latest:
        return JsonResponse({
            "latest": None,
            "total": 0
        })

    return JsonResponse({
        "latest": {
            "id": latest.id,
            "date": latest.created_at.strftime("%d %B %Y"),
            "symptoms": latest.symptoms,
            "observations": latest.observations,
            "diagnosis": latest.diagnosis_notes,
            "follow_up": latest.follow_up_notes,
        },
        "total": records.count()
    })
    
@login_required
def patient_chatbot_prescriptions(request):

    patient = request.user.patient

    prescriptions = Prescription.objects.filter(
        patient=patient
    ).order_by("-created_at")

    if not prescriptions.exists():
        return JsonResponse({
            "latest": None,
            "total": 0
        })

    latest = prescriptions.first()

    return JsonResponse({
        "latest": {
            "id": latest.id,
            "date": latest.created_at.strftime("%d %B %Y"),
            "medicine_name": latest.medicine_name,
            "dosage": latest.dosage,
            "frequency": latest.frequency,
            "duration": latest.duration,
            "instructions": latest.instructions,
            "medicine_given": latest.medicine_given,
            "status": latest.status,
        },
        "total": prescriptions.count()
    })

@login_required
def patient_chatbot_bills(request):

    patient = request.user.patient

    bills = Bill.objects.filter(
        patient=patient
    ).order_by("-created_at")

    if not bills.exists():
        return JsonResponse({
            "latest": None,
            "total": 0
        })

    latest = bills.first()

    return JsonResponse({
        "latest": {
            "id": latest.id,
            "date": latest.created_at.strftime("%d %B %Y"),
            "total_amount": str(latest.total_amount),
            "consultation_fee": str(latest.consultation_fee),
            "medicine_fee": str(latest.medicine_fee),
        },
        "total": bills.count()
    })

@login_required
def patient_chatbot_history(request):

    patient = request.user.patient

    appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__lt=timezone.localdate()
    ).order_by(
        "-appointment_date",
        "-appointment_time"
    )

    total_visits = Appointment.objects.filter(
        patient=patient
    ).count()

    completed_visits = Appointment.objects.filter(
        patient=patient,
        status="completed"
    ).count()

    last_visit = appointments.first()

    if not last_visit:
        return JsonResponse({
            "latest": None,
            "total_visits": total_visits,
            "completed_visits": completed_visits
        })

    return JsonResponse({
        "latest": {
            "appointment_no": last_visit.appointment_no,
            "date": last_visit.appointment_date.strftime(
                "%d %B %Y"
            ),
            "time": (
                last_visit.appointment_time.strftime("%I:%M %p")
                if last_visit.appointment_time
                else "Time not specified"
            ),
            "reason": last_visit.reason_for_visit,
            "status": last_visit.get_status_display(),
        },

        "total_visits": total_visits,

        "completed_visits": completed_visits,
    })


@login_required
def patient_dashboard(request):

    patient = request.user.patient
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).order_by("-created_at")

    appointments = Appointment.objects.filter(
        patient=patient
    )

    total_bill = Bill.objects.filter(
        patient=patient
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    recent_appointments = appointments.order_by(
        "-appointment_date"
    )[:5]

    context = {

        "patient": patient,

        "total_appointments": appointments.count(),

        "completed_appointments":
            appointments.filter(
                status="completed"
            ).count(),

        "cancelled_appointments":
            appointments.filter(
                status="cancelled"
            ).count(),

        "total_bill": total_bill,

        "recent_appointments": recent_appointments,

        "notifications": notifications,

        "notification_count": notifications.count(),

    }

    return render(
        request,
        "patients/dashboard.html",
        context,
    )


from django.db.models import Q

@login_required
def patient_appointments(request):

    patient = request.user.patient

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-appointment_date")

    search = request.GET.get("search")

    if search:
        appointments = appointments.filter(
            Q(reason_for_visit__icontains=search) |
            Q(status__icontains=search) |
            Q(appointment_date__icontains=search)
        )

    return render(
        request,
        "patients/appointments.html",
        {
            "appointments": appointments,
            "patient": patient,
        },
    )

@login_required
def cancel_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.status = "cancelled"

    appointment.cancelled_by = "patient"

    appointment.save()

    return redirect(
        "patient_appointments"
    )

from django.shortcuts import render
from doctors.models import MedicalRecord
from prescriptions.models import Prescription


from django.db.models import Q
from prescriptions.models import Prescription
from doctors.models import MedicalRecord


def medical_records(request):

    patient = request.user.patient


    records = MedicalRecord.objects.filter(
        patient=patient
    ).order_by(
        "-created_at"
    )


    # SEARCH FUNCTIONALITY

    query = request.GET.get("q")


    if query:

        records = records.filter(

            Q(diagnosis_notes__icontains=query) |
            Q(symptoms__icontains=query) |
            Q(observations__icontains=query) |
            Q(follow_up_notes__icontains=query)

        )



    total_records = MedicalRecord.objects.filter(
        patient=patient
    ).count()



    last_visit = MedicalRecord.objects.filter(
        patient=patient
    ).order_by(
        "-created_at"
    ).first()



    total_medicines = Prescription.objects.filter(
        patient=patient
    ).count()



    context = {
        "patient": patient,

        "records": records,

        "total_records": total_records,

        "last_visit": last_visit,

        "total_medicines": total_medicines,

    }


    return render(
        request,
        "patients/records.html",
        context
    )

@login_required
def patient_prescriptions(request):

    patient = request.user.patient

    prescriptions = Prescription.objects.filter(
        patient=patient
    ).order_by("-created_at")

    return render(
        request,
        "patients/prescriptions.html",
        {
            "patient": patient,
            "prescriptions": prescriptions,
        },
    )

from django.db.models import Sum


@login_required
def patient_bills(request):

    patient = request.user.patient

    bills = Bill.objects.filter(
        patient=patient
    ).order_by("-created_at")


    total_bill = bills.aggregate(
        total=Sum("total_amount")
    )["total"] or 0


    total_consultation = bills.aggregate(
        total=Sum("consultation_fee")
    )["total"] or 0


    total_medicine = bills.aggregate(
        total=Sum("medicine_fee")
    )["total"] or 0



    return render(
        request,
        "patients/bills.html",
        {
            "patient": patient,

            "bills": bills,

            "total_bill": total_bill,

            "total_consultation": total_consultation,

            "total_medicine": total_medicine,
        },
    )


@login_required
def patient_settings(request):

    patient = request.user.patient

    return render(
        request,
        "patients/settings.html",
        {
            "patient": patient,
        },
    )





@login_required
def patient_profile(request):
    patient = request.user.patient

    if request.method == "POST":
    
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()

            # Keep User model in sync
            request.user.first_name = patient.full_name.split()[0]

            if len(patient.full_name.split()) > 1:
                request.user.last_name = " ".join(patient.full_name.split()[1:])
            else:
                request.user.last_name = ""

            request.user.email = patient.email
            request.user.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("patient_profile")

    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        "patients/profile.html",
        {
            "patient": patient,
            "form": form,
        },
    )

@login_required
def patient_change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check current password
        if not request.user.check_password(current_password):

            messages.error(
                request,
                "Current password is incorrect."
            )

        # Check both passwords match
        elif new_password != confirm_password:

            messages.error(
                request,
                "New passwords do not match."
            )

        # Check minimum length
        elif len(new_password) < 8:

            messages.error(
                request,
                "Password must be at least 8 characters long."
            )

        else:

            request.user.set_password(new_password)
            request.user.save()

            # Keep user logged in
            update_session_auth_hash(request, request.user)

            messages.success(
                request,
                "Password updated successfully."
            )

            return redirect("patient_change_password")

    return render(
        request,
        "patients/change_password.html",
        {
            "patient": request.user.patient,
        }
    )

from prescriptions.models import Prescription

@login_required
def patient_history(request):

    patient = request.user.patient


    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by(
        "-appointment_date"
    )


    total_visits = appointments.count()


    completed_visits = appointments.filter(
        status="completed"
    ).count()


    last_visit = appointments.first()



    return render(
        request,
        "patients/history.html",
        {
            "patient": patient,

            "appointments": appointments,

            "total_visits": total_visits,

            "completed_visits": completed_visits,

            "last_visit": last_visit,
        },
    )