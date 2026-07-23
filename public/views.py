from django.shortcuts import render
from appointments.models import AppointmentRequest
from django.shortcuts import render, redirect
from patients.models import Patient
from appointments.models import Appointment

def home(request):
    return render(request, 'public/home.html')

def about(request):
    return render(request, 'public/about.html')

def services(request):
    return render(request, 'public/services.html')

def book_appointment(request):

    success = None
    request_type = None

    if request.method == "POST":

        request_type = request.POST.get("request_type")

        # -----------------------------
        # NEW PATIENT
        # -----------------------------
        if request_type == "new":

            AppointmentRequest.objects.create(
                request_type="new",
                full_name=request.POST.get("full_name"),
                phone=request.POST.get("phone"),
                email=request.POST.get("email"),
                age=request.POST.get("age"),
                gender=request.POST.get("gender"),
                address=request.POST.get("address"),
                preferred_date=request.POST.get("preferred_date"),
                reason_for_visit=request.POST.get("reason_for_visit")
            )

            success = "Appointment request submitted successfully."

        # -----------------------------
        # EXISTING PATIENT
        # -----------------------------
        else:

            patient = Patient.objects.filter(
                patient_id=request.POST.get("patient_id"),
                phone=request.POST.get("phone")
            ).first()

            if patient:

                Appointment.objects.create(
                    patient=patient,
                    appointment_date=request.POST.get("preferred_date"),
                    reason_for_visit=request.POST.get("reason_for_visit"),
                    status="pending"
                )

                success = "Follow-up appointment booked successfully."

            else:

                success = "Invalid Patient ID or Phone Number."

    return render(
        request,
        "public/appointment.html",
        {
            "success": success,
            "request_type": request_type
        }
    )
def patient_status(request):

    appointment = None
    error = None

    if request.method == "POST":

        patient_id = request.POST.get("patient_id")
        phone = request.POST.get("phone")

        try:

            patient = Patient.objects.get(
                patient_id=patient_id,
                phone=phone
            )

            appointment = Appointment.objects.filter(
                patient=patient
            ).order_by('-appointment_date').first()

        except Patient.DoesNotExist:

            error = "No patient found with the provided Patient ID and Phone Number."
            

    return render(
    request,
    'public/patient_status.html',
    {
        'appointment': appointment,
        'error': error
    }
)