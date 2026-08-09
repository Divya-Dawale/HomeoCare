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
from accounts.models import User
from notifications.utils import notify_doctors
from django.utils import timezone
from notifications.utils import notify_patient
from notifications.email_utils import send_appointment_email
from notifications.email_utils import (
    send_appointment_email,
    send_appointment_cancelled_email,
)
from django.contrib import messages
from .forms import ReceptionistProfileForm
from appointments.utils import (
    get_next_appointment_no,
    get_appointment_time,
)
def dashboard(request):

    pending_requests = AppointmentRequest.objects.filter(
        status="pending",
        preferred_date=date.today()
    ).count()

    notifications = request.user.notifications.filter(
        is_read=False,
        created_at__date=timezone.now().date()
    ).order_by("-created_at")
    notification_count = notifications.count()
    
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

    "notifications": notifications,

    "notification_count": notifications.count(),

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

    from django.db.models import Q

    if search:
            appointments = appointments.filter(
                Q(patient__full_name__icontains=search) |
                Q(patient__patient_id__icontains=search) |
                Q(patient__phone__icontains=search)
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

    if appointment.status == "waiting":

        appointment.status = "cancelled"
        appointment.cancelled_by = "receptionist"
        appointment.save()

        notify_patient(
            appointment.patient,
            f"Your appointment on {appointment.appointment_date} has been cancelled by the receptionist."
        )
        notify_doctors(
            f"Appointment for {appointment.patient.full_name} on {appointment.appointment_date} has been cancelled by the receptionist."
        )
        send_appointment_cancelled_email(
            appointment.patient.email,
            appointment.patient.full_name,
            appointment.appointment_date
        )

    return redirect("appointments")
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

        # Create login account for patient
        if not User.objects.filter(username=patient.patient_id).exists():

            user = User.objects.create_user(
                username=patient.patient_id,
                password=patient.patient_id,
                first_name=patient.full_name,
                email=patient.email,
                role="patient",
                phone=patient.phone,
            )
            patient.user = user
            patient.save()

            user.is_active = True
            user.save()

    # Create appointment
    appointment_no = get_next_appointment_no(
        appointment_request.preferred_date
    )

    Appointment.objects.create(
        patient=patient,
        appointment_no=appointment_no,
        appointment_time=get_appointment_time(
            appointment_request.preferred_date,
            appointment_no
        ),
        appointment_date=appointment_request.preferred_date,
        reason_for_visit=appointment_request.reason_for_visit,
        status="waiting"
    )

    # Mark request as approved
    appointment_request.status = "approved"
    appointment_request.save()
    send_appointment_email(
        patient.email,
        patient.full_name,
        appointment_request.preferred_date
    )
    notify_doctors(
    f"New appointment approved for {patient.full_name}."
    )
    return redirect(
        "appointment_requests"
    )
from django.db import transaction
from datetime import date
from doctors.models import DoctorSettings


def approve_all_requests(request):

    if request.method != "POST":
        return redirect("appointment_requests")

    today = date.today()

    # Get doctor's settings
    doctor_settings = DoctorSettings.objects.first()

    if not doctor_settings:
        messages.error(
            request,
            "Doctor settings could not be found."
        )
        return redirect("appointment_requests")

    # --------------------------------------------------
    # COUNT TODAY'S ALREADY BOOKED APPOINTMENTS
    # --------------------------------------------------

    existing_appointments = Appointment.objects.filter(
        appointment_date=today
    ).count()

    # --------------------------------------------------
    # REMAINING CAPACITY
    # --------------------------------------------------

    remaining_slots = (
        doctor_settings.max_patients_per_day
        - existing_appointments
    )

    if remaining_slots <= 0:

        messages.warning(
            request,
            "Today's appointment limit has already been reached."
        )

        return redirect("appointment_requests")

    # --------------------------------------------------
    # GET PENDING REQUESTS
    # FIRST COME = OLDEST CREATED_AT FIRST
    # --------------------------------------------------

    pending_requests = AppointmentRequest.objects.filter(
        request_type="new",
        status="pending",
        preferred_date=today
    ).order_by("created_at")

    approved_count = 0

    # --------------------------------------------------
    # APPROVE REQUESTS ONE BY ONE
    # --------------------------------------------------

    for appointment_request in pending_requests:

        # Stop when today's capacity is full
        if approved_count >= remaining_slots:
            break

        with transaction.atomic():

            # ------------------------------------------
            # CHECK IF PATIENT ALREADY EXISTS
            # ------------------------------------------

            patient = Patient.objects.filter(
                phone=appointment_request.phone
            ).first()

            # ------------------------------------------
            # CREATE PATIENT IF NOT FOUND
            # ------------------------------------------

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

                # --------------------------------------
                # CREATE PATIENT LOGIN
                # --------------------------------------

                if not User.objects.filter(
                    username=patient.patient_id
                ).exists():

                    user = User.objects.create_user(
                        username=patient.patient_id,
                        password=patient.patient_id,
                        first_name=patient.full_name,
                        email=patient.email,
                        role="patient",
                        phone=patient.phone,
                    )

                    patient.user = user
                    patient.save()

                    user.is_active = True
                    user.save()

            # ------------------------------------------
            # CREATE APPOINTMENT
            # ------------------------------------------

            appointment_no = get_next_appointment_no(
                appointment_request.preferred_date
            )

            Appointment.objects.create(
                patient=patient,
                appointment_no=appointment_no,
                appointment_time=get_appointment_time(
                    appointment_request.preferred_date,
                    appointment_no
                ),
                appointment_date=appointment_request.preferred_date,
                reason_for_visit=appointment_request.reason_for_visit,
                status="waiting"
            )

            # ------------------------------------------
            # MARK REQUEST APPROVED
            # ------------------------------------------

            appointment_request.status = "approved"
            appointment_request.save()

            # ------------------------------------------
            # SEND EMAIL
            # ------------------------------------------

            send_appointment_email(
                patient.email,
                patient.full_name,
                appointment_request.preferred_date
            )

            # ------------------------------------------
            # NOTIFY DOCTOR
            # ------------------------------------------

            notify_doctors(
                f"New appointment approved for "
                f"{patient.full_name}."
            )

            approved_count += 1

    # --------------------------------------------------
    # RESULT MESSAGE
    # --------------------------------------------------

    if approved_count == 0:

        messages.info(
            request,
            "There are no pending appointment requests to approve."
        )

    elif approved_count < pending_requests.count():

        messages.success(
            request,
            f"{approved_count} appointment request(s) "
            f"approved. Today's remaining capacity has been reached. "
            f"Other requests remain pending."
        )

    else:

        messages.success(
            request,
            f"{approved_count} appointment request(s) "
            f"approved successfully."
        )

    return redirect("appointment_requests")
def start_consultation(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.status = "consulting"
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

    if request.method == "POST":

        form = ReceptionistProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                 request,
                "Profile updated successfully."
                )

            return redirect(
                "receptionist_profile"
            )

    else:

        form = ReceptionistProfileForm(
            instance=request.user
        )

    return render(
        request,
        "receptionist/profile.html",
        {
            "form": form
        }
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

from patients.models import Patient
from appointments.models import Appointment
from .forms import PatientAppointmentForm


def add_patient(request):

    success = None
    search_result = None

    form = PatientAppointmentForm()

    if request.method == "POST":

        # NEW PATIENT

        if "register_patient" in request.POST:

            form = PatientAppointmentForm(
                request.POST
            )

            if form.is_valid():

                patient = form.save()

                appointment_date = form.cleaned_data[
                    "appointment_date"
                ]

                appointment_no = get_next_appointment_no(
                    appointment_date
                )

                Appointment.objects.create(
                    patient=patient,

                    appointment_no=appointment_no,

                    appointment_time=get_appointment_time(
                        appointment_date,
                        appointment_no
                    ),

                    appointment_date=appointment_date,

                    reason_for_visit=form.cleaned_data[
                        "reason_for_visit"
                    ],

                    status="waiting"
                )

                success = (
                    f"Patient Registered "
                    f"({patient.patient_id})"
                )

                form = PatientAppointmentForm()

            else:

                print(form.errors)

        # SEARCH EXISTING PATIENT

        elif "search_patient" in request.POST:

            search = request.POST.get(
                "search"
            )

            search_result = Patient.objects.filter(
                patient_id__icontains=search
            ).first()

        # BOOK APPOINTMENT FOR EXISTING PATIENT

        elif "book_existing" in request.POST:

            patient_id = request.POST.get(
                "patient_id"
            )

            patient = Patient.objects.get(
                id=patient_id
            )

            appointment_date = request.POST.get(
                "appointment_date"
            )

            appointment_no = get_next_appointment_no(
                appointment_date
            )

            Appointment.objects.create(
                patient=patient,

                appointment_no=appointment_no,

                appointment_time=get_appointment_time(
                    appointment_date,
                    appointment_no
                ),

                appointment_date=appointment_date,

                reason_for_visit=request.POST.get(
                    "reason_for_visit"
                ),

                status="waiting"
            )

            success = (
                f"Appointment Booked "
                f"for {patient.patient_id}"
            )

    return render(

        request,

        "receptionist/add_patient.html",

        {

            "form": form,

            "success": success,

            "search_result": search_result

        }

    )

