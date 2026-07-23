from django.shortcuts import render
from appointments.models import AppointmentRequest, Appointment
from patients.models import Patient
from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404, redirect

def dashboard(request):

    pending_requests = AppointmentRequest.objects.filter(
        status="pending"
    ).count()

    approved_appointments = Appointment.objects.filter(
        status="approved"
    ).count()

    total_patients = Patient.objects.count()

    today_appointments = Appointment.objects.count()

    recent_requests = AppointmentRequest.objects.order_by(
        "-created_at"
    )[:5]

    context = {
        "pending_requests": pending_requests,
        "approved_appointments": approved_appointments,
        "total_patients": total_patients,
        "today_appointments": today_appointments,
        "recent_requests": recent_requests,
    }

    return render(
        request,
        "receptionist/dashboard.html",
        context,
    )


def appointment_requests(request):

    requests = AppointmentRequest.objects.filter(
        request_type="new",
        status="pending"
    ).order_by("-created_at")

    return render(
        request,
        "receptionist/appointment_requests.html",
        {"requests": requests},
    )

def patient_detail(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    return render(
        request,
        "receptionist/patient_detail.html",
        {
            "patient": patient
        }
    )
from patients.models import Patient

def patients(request):

    patients = Patient.objects.all().order_by("patient_id")

    return render(
        request,
        "receptionist/patients.html",
        {
            "patients": patients
        }
    )


def appointments(request):
    return render(
        request,
        "receptionist/appointments.html"
    )
def request_detail(request, request_id):

    appointment_request = get_object_or_404(
        AppointmentRequest,
        id=request_id
    )

    return render(
        request,
        "receptionist/request_detail.html",
        {
            "appointment_request": appointment_request
        }
    )
def reject_request(request, request_id):

    appointment_request = get_object_or_404(
        AppointmentRequest,
        id=request_id
    )

    appointment_request.status = "rejected"
    appointment_request.save()

    return redirect("appointment_requests")
def approve_request(request, request_id):

    appointment_request = get_object_or_404(
        AppointmentRequest,
        id=request_id
    )

    # If already approved, do nothing
    if appointment_request.status == "approved":
        return redirect("appointment_requests")

    # Check if patient already exists
    patient = Patient.objects.filter(
        phone=appointment_request.phone
    ).first()

    # Create new patient if not found
    if not patient:

        last_patient = Patient.objects.order_by("-id").first()

        if last_patient:
            last_number = int(last_patient.patient_id.replace("HC", ""))
            new_id = f"HC{last_number + 1:04d}"
        else:
            new_id = "HC0001"

        patient = Patient.objects.create(
            patient_id=new_id,
            full_name=appointment_request.full_name,
            phone=appointment_request.phone,
            email=appointment_request.email,
            age=appointment_request.age,
            gender=appointment_request.gender,
            address=appointment_request.address,
        )

    # Create Appointment
    Appointment.objects.create(
        patient=patient,
        appointment_date=appointment_request.preferred_date,
        reason_for_visit=appointment_request.reason_for_visit,
        status="approved"
    )

    # Update request status
    appointment_request.status = "approved"
    appointment_request.save()

    return redirect("appointment_requests")