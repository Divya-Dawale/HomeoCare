from django.shortcuts import render
from appointments.models import AppointmentRequest, Appointment
from patients.models import Patient
from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from datetime import date

from datetime import date

def dashboard(request):

    pending_requests = AppointmentRequest.objects.filter(
        status="pending",
        preferred_date=date.today()
    ).count()

    approved_appointments = Appointment.objects.filter(
    appointment_date=date.today(),
    status="completed"
    ).count()

    total_patients = Patient.objects.count()

    today_appointments = Appointment.objects.filter(
        appointment_date=date.today()
    ).count()

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

from appointments.models import Appointment

def patient_detail(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-appointment_date")

    return render(
        request,
        "receptionist/patient_detail.html",
        {
            "patient": patient,
            "appointments": appointments,
        }
    )
from patients.models import Patient
def edit_patient(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == "POST":

        patient.full_name = request.POST.get("full_name")
        patient.phone = request.POST.get("phone")
        patient.email = request.POST.get("email")
        patient.age = request.POST.get("age")
        patient.gender = request.POST.get("gender")
        patient.address = request.POST.get("address")

        patient.save()

        return redirect(
            "patient_detail",
            patient_id=patient.id
        )

    return render(
        request,
        "receptionist/edit_patient.html",
        {
            "patient": patient
        }
    )
from django.db.models import Q

def patients(request):

    search = request.GET.get("search")

    patients = Patient.objects.all().order_by("-id")

    if search:

        patients = patients.filter(
            Q(full_name__icontains=search) |
            Q(patient_id__icontains=search) |
            Q(phone__icontains=search)
        )

    return render(
        request,
        "receptionist/patients.html",
        {
            "patients": patients,
            "search": search
        }
    )


from appointments.models import Appointment



def appointments(request):

    status = request.GET.get("status")
    search = request.GET.get("search")

    appointments = Appointment.objects.filter(
    appointment_date=date.today()
    ).order_by(
    "created_at"
    )

    if status:

        appointments = appointments.filter(
            status=status
        )

    if search:

        appointments = appointments.filter(
            patient__full_name__icontains=search
        ) | appointments.filter(
            patient__patient_id__icontains=search
        ) | appointments.filter(
            patient__phone__icontains=search
        )

    return render(
        request,
        "receptionist/appointments.html",
        {
            "appointments": appointments,
            "selected_status": status,
            "search": search
        }
    )
from django.shortcuts import get_object_or_404, redirect
from appointments.models import Appointment

def cancel_appointment(
    request,
    appointment_id
):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.status = "cancelled"

    appointment.save()

    return redirect(
        "appointments"
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

    # Already approved
    if appointment_request.status == "approved":
        return redirect("appointment_requests")

    # Check if patient already exists
    patient = Patient.objects.filter(
        phone=appointment_request.phone
    ).first()

    # Create patient if not found
    if not patient:

        last_patient = Patient.objects.order_by(
            "-id"
        ).first()

        if last_patient:

            last_number = int(
                last_patient.patient_id.replace(
                    "HC",
                    ""
                )
            )

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

    # Create appointment
    Appointment.objects.create(
        patient=patient,
        appointment_date=appointment_request.preferred_date,
        reason_for_visit=appointment_request.reason_for_visit,
        status="waiting"
    )

    # Mark request as approved
    appointment_request.status = "approved"
    appointment_request.save()

    return redirect(
        "appointment_requests"
    )
def start_consultation(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.status = "consulting"
    appointment.save()

    return redirect("appointments")


def complete_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.status = "completed"
    appointment.save()

    return redirect("appointments")

from prescriptions.models import Prescription
from prescriptions.models import Prescription
from django.db.models import Q

def prescriptions(request):

    status = request.GET.get("status")
    search = request.GET.get("search")

    prescriptions = Prescription.objects.select_related(
    "patient",
    "appointment"
    ).filter(
    appointment__appointment_date=date.today()
    ).order_by("-created_at")

    if status:
        prescriptions = prescriptions.filter(
            status=status
        )

    if search:
        prescriptions = prescriptions.filter(
            Q(patient__full_name__icontains=search) |
            Q(patient__patient_id__icontains=search)
        )

    pending_count = Prescription.objects.filter(
    appointment__appointment_date=date.today(),
    status="pending"
    ).count()

    given_count = Prescription.objects.filter(
    appointment__appointment_date=date.today(),
    status="given"
    ).count()

    context = {
        "prescriptions": prescriptions,
        "pending_count": pending_count,
        "given_count": given_count,
        "total_count": pending_count + given_count,
        "selected_status": status,
        "search": search,
    }

    return render(
        request,
        "receptionist/prescriptions.html",
        context
    )
def mark_medicine_given(
    request,
    prescription_id
):

    prescription = get_object_or_404(
        Prescription,
        id=prescription_id
    )

    prescription.medicine_given = True

    prescription.status = "given"

    prescription.save()

    return redirect(
        "receptionist_prescriptions"
    )

def settings(request):

    return render(
        request,
        "receptionist/settings.html"
    )

@login_required
def profile(request):

    return render(
        request,
        "receptionist/profile.html"
    )

@login_required
def edit_profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect(
                "receptionist_settings"
            )

    else:

        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "receptionist/edit_profile.html",
        {
            "form": form
        }
    )


def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        print("FORM VALID:", form.is_valid())

        if form.is_valid():

            print("PASSWORD CHANGED")

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            return redirect(
                "receptionist_settings"
            )

        else:

            print(form.errors)

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "receptionist/change_password.html",
        {
            "form": form
        }
    )