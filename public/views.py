from django.shortcuts import render
from appointments.models import AppointmentRequest
from django.shortcuts import render, redirect
from patients.models import Patient
from appointments.models import Appointment
from doctors.models import DoctorSettings
from appointments.models import Appointment

def home(request):
    return render(request, 'public/home.html')

def about(request):
    return render(request, 'public/about.html')

def services(request):
    return render(request, 'public/services.html')
from datetime import date
def book_appointment(request):

    success = None
    error_message = None
    request_type = None
    doctor_settings = DoctorSettings.objects.first()

    today_count = AppointmentRequest.objects.filter(
                preferred_date=date.today()
                ).count()

    booking_closed = (
          doctor_settings and
              today_count >= doctor_settings.max_patients_per_day
                  )
    
    if request.method == "POST":

        request_type = request.POST.get(
            "request_type"
        )
        if booking_closed:

            error_message = (
                 "Today's appointment booking limit has been reached."
            )

            return render(
                request,
                "public/appointment.html",
                        {
                    "error_message": error_message,
                    "request_type": request_type,
                    "booking_closed": booking_closed,
                }
            )
    
    

        # -----------------------------
        # NEW PATIENT
        # -----------------------------
        if request_type == "new":

            AppointmentRequest.objects.create(

                request_type="new",

                full_name=request.POST.get(
                    "full_name"
                ),

                phone=request.POST.get(
                    "phone"
                ),

                email=request.POST.get(
                    "email"
                ),

                age=request.POST.get(
                    "age"
                ),

                gender=request.POST.get(
                    "gender"
                ),

                address=request.POST.get(
                    "address"
                ),

                preferred_date=date.today(),

                reason_for_visit=request.POST.get(
                    "reason_for_visit"
                )

            )
            print("NEW REQUEST SAVED")
            success = (
                "Appointment request submitted successfully."
            )

        # -----------------------------
        # EXISTING PATIENT
        # -----------------------------
        else:

            patient = Patient.objects.filter(

                patient_id=request.POST.get(
                    "patient_id"
                ),

                phone=request.POST.get(
                    "phone"
                )

            ).first()

            if patient:

                AppointmentRequest.objects.create(

                    request_type="existing",

                    patient_id=patient.patient_id,

                    full_name=patient.full_name,

                    phone=patient.phone,

                    email=patient.email,

                    age=patient.age,

                    gender=patient.gender,

                    address=patient.address,

                    preferred_date=date.today(),

                    reason_for_visit=request.POST.get(
                        "reason_for_visit"
                    )

                )
                
                success = (
                    "Follow-up appointment booked successfully."
                )

            else:

                error_message = (
                    "Invalid Patient ID or Phone Number."
                )

    return render(
        request,
        "public/appointment.html",
        {
            "success": success,
            "error_message": error_message,
            "request_type": request_type,
            "booking_closed": booking_closed,
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
from doctors.models import DoctorSettings



def contact(request):

    settings = DoctorSettings.objects.first()


    return render(
        request,
        "public/contact.html",
        {
            "settings": settings
        }
    )