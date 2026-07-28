from django.shortcuts import render
from appointments.models import Appointment
from django.shortcuts import render, get_object_or_404
from .models import MedicalHistory
from django.shortcuts import redirect
from .forms import MedicalHistoryForm
from .forms import MedicalRecordForm
from prescriptions.forms import PrescriptionForm
from prescriptions.models import Prescription

def doctor_dashboard(request):

    return render(
        request,
        'doctor/dashboard.html'
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

    appointments = Appointment.objects.filter(
        status="waiting"
    ).order_by("appointment_date")

    context = {
        "appointments": appointments
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
    previous_visits = patient.medical_records.all().order_by("-created_at")
    previous_prescriptions = patient.prescriptions.all().order_by( "-created_at")
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

