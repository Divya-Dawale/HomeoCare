from django.shortcuts import render
from appointments.models import Appointment
from django.shortcuts import render, get_object_or_404
from .models import MedicalHistory
from django.shortcuts import redirect
from .forms import MedicalHistoryForm
from .forms import MedicalRecordForm
from prescriptions.forms import PrescriptionForm
from prescriptions.models import Prescription
from doctors.models import MedicalRecord
from django.utils import timezone
from datetime import date
from billing.models import Bill
from datetime import date, timedelta
from django.db.models import Sum, Max, Min, Avg
from django.db.models.functions import TruncDate
from django.db.models import Sum
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from accounts.models import User
from .forms import DoctorProfileForm


def doctor_dashboard(request):

    today = timezone.now().date()

    waiting_patients = Appointment.objects.filter(
        appointment_date=today,
        status="waiting"
    ).count()

    consulting_patients = Appointment.objects.filter(
        appointment_date=today,
        status="consulting"
    ).count()

    completed_today = Appointment.objects.filter(
        appointment_date=today,
        status="completed"
    ).count()

    total_records = Appointment.objects.filter(
        status="completed"
    ).count()
    context = {
        "waiting_patients": waiting_patients,
        "consulting_patients": consulting_patients,
        "completed_today": completed_today,
        "total_records": total_records,
    }

    return render(
        request,
        "doctor/dashboard.html",
        context
    )  


def patient_queue(request):

    return render(
        request,
        'doctor/patient_queue.html'
    )


def medical_records(request):

    return render(
        request,
        'doctor/patient_history.html'
    )


def prescriptions(request):

    return render(
        request,
        'doctor/prescription.html'
    )

def patient_queue(request):

    status = request.GET.get("status")

    appointments = Appointment.objects.filter(
    appointment_date=date.today()
    ).order_by(
    "created_at"
    )

    if status:
        appointments = appointments.filter(
            status=status
        )

    context = {
        "appointments": appointments,
        "selected_status": status,
    }

    return render(
        request,
        "doctor/patient_queue.html",
        context
    )

def consultation(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    patient = appointment.patient

    # Automatically move patient to Consulting
    if appointment.status == "waiting":

        appointment.status = "consulting"

        appointment.save()

    try:
        history = MedicalHistory.objects.get(
            patient=patient
        )

    except MedicalHistory.DoesNotExist:
        history = None

    record_form = MedicalRecordForm()
    prescription_form = PrescriptionForm()

    if request.method == "POST":

        # Save Medical Record
        if "save_record" in request.POST:

            record_form = MedicalRecordForm(
                request.POST
            )

            if record_form.is_valid():

                record = record_form.save(
                    commit=False
                )

                record.patient = patient
                record.appointment = appointment

                record.save()

                return redirect(
                    "consultation",
                    appointment_id=appointment.id
                )

        # Save Prescription
        elif "save_prescription" in request.POST:

            prescription_form = PrescriptionForm(
                request.POST
            )

            if prescription_form.is_valid():

                latest_record = patient.medical_records.last()

                if latest_record:

                    prescription = prescription_form.save(
                        commit=False
                    )

                    prescription.patient = patient
                    prescription.appointment = appointment
                    prescription.medical_record = latest_record

                    prescription.save()

                return redirect(
                    "consultation",
                    appointment_id=appointment.id
                )

        # Complete Consultation
        elif "complete_consultation" in request.POST:

            prescription_exists = Prescription.objects.filter(
                appointment=appointment
            ).exists()

            if prescription_exists:

                appointment.status = "completed"

                appointment.save()

                return redirect(
                    "patient_queue"
                )

    previous_visits = patient.medical_records.all().order_by(
        "-created_at"
    )

    previous_prescriptions = patient.prescriptions.all().order_by(
        "-created_at"
    )

    context = {

        "appointment": appointment,

        "patient": patient,

        "history": history,

        "record_form": record_form,

        "prescription_form": prescription_form,

        "previous_visits": previous_visits,

        "previous_prescriptions": previous_prescriptions,

    }

    return render(
        request,
        "doctor/consultation.html",
        context
    )

    

def create_medical_history(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    patient = appointment.patient

    if request.method == "POST":

        form = MedicalHistoryForm(
            request.POST
        )

        if form.is_valid():

            history = form.save(
                commit=False
            )

            history.patient = patient

            history.save()

            return redirect(
                "consultation",
                appointment_id=appointment.id
            )

    else:

        form = MedicalHistoryForm()

    return render(

        request,

        "doctor/create_history.html",

        {
            "form": form,
            "patient": patient
        }

    )

def doctor_revenue(request):

    today = date.today()

    bills = Bill.objects.filter(
        payment_status="paid"
    )

    filter_type = request.GET.get("filter")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if filter_type == "today":

        bills = bills.filter(
            created_at__date=today
        )

    elif filter_type == "7days":

        bills = bills.filter(
            created_at__date__gte=today - timedelta(days=7)
        )

    elif filter_type == "15days":

        bills = bills.filter(
            created_at__date__gte=today - timedelta(days=15)
        )

    elif filter_type == "month":

        bills = bills.filter(
            created_at__year=today.year,
            created_at__month=today.month
        )

    elif filter_type == "year":

        bills = bills.filter(
            created_at__year=today.year
        )

    elif filter_type == "all":

        pass

    if start_date and end_date:

        bills = bills.filter(
            created_at__date__range=[
                start_date,
                end_date
            ]
        )

    revenue = bills.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    consultation_revenue = bills.aggregate(
        total=Sum("consultation_fee")
    )["total"] or 0

    medicine_revenue = bills.aggregate(
        total=Sum("medicine_fee")
    )["total"] or 0

    total_bills = bills.count()

    average_bill = bills.aggregate(
        avg=Avg("total_amount")
    )["avg"] or 0

    highest_bill = bills.aggregate(
        highest=Max("total_amount")
    )["highest"] or 0

    lowest_bill = bills.aggregate(
        lowest=Min("total_amount")
    )["lowest"] or 0

    chart_data = (
          bills
          .annotate(day=TruncDate("created_at"))
          .values("day")
          .annotate(total=Sum("total_amount"))
          .order_by("day")
      )

    revenue_labels = [
          item["day"].strftime("%d %b")
          for item in chart_data
    ]

    revenue_values = [
          float(item["total"])
          for item in chart_data
    ]
    context = {

        "revenue": revenue,

        "consultation_revenue": consultation_revenue,

        "medicine_revenue": medicine_revenue,

        "total_bills": total_bills,

        "average_bill": average_bill,

        "highest_bill": highest_bill,

        "lowest_bill": lowest_bill,

        "selected_filter": filter_type,

        "revenue_labels": revenue_labels,
         
        "revenue_values": revenue_values,

        "bills": bills.order_by("-created_at")

    }

    return render(
        request,
        "doctor/revenue.html",
        context
    )
from .models import DoctorSettings
from .forms import DoctorSettingsForm
from django.contrib.auth.decorators import login_required

@login_required
def doctor_settings(request):

    print(request.user)
    print(request.user.is_authenticated)
    settings_obj, created = (
        DoctorSettings.objects.get_or_create(
            doctor=request.user
        )
    )

    if request.method == "POST":

        form = DoctorSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            form.save()

            return redirect(
                "doctor_settings"
            )

    else:

        form = DoctorSettingsForm(
            instance=settings_obj
        )

    return render(
        request,
        "doctor/settings.html",
        {
            "form": form
        }
    )


def edit_doctor_profile(request):

    if request.method == "POST":

        form = DoctorProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect(
                "doctor_settings"
            )

    else:

        form = DoctorProfileForm(
            instance=request.user
        )

    return render(
        request,
        "doctor/edit_profile.html",
        {
            "form": form
        }
    )
def doctor_change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            print("VALID")

            user = form.save()

            update_session_auth_hash(
            request,
            user
            )

            return redirect("doctor_settings")

        else:

            print(form.errors)

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            return redirect(
                "doctor_settings"
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "doctor/change_password.html",
        {
            "form": form
        }
    )