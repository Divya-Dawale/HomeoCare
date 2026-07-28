from django.shortcuts import render
from appointments.models import Appointment
from django.shortcuts import render, get_object_or_404
from .models import MedicalHistory
from django.shortcuts import redirect
from .forms import MedicalHistoryForm
from .forms import MedicalRecordForm

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

    context = {
        "appointment": appointment,
        "patient": appointment.patient,
    }

    record_form = MedicalRecordForm()
    
    return render(
        request,
        "doctor/consultation.html",
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

    context = {

        "appointment": appointment,

        "patient": patient,

        "history": history,

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

    if MedicalHistory.objects.filter(patient=patient).exists():

        return redirect(
            "consultation",
            appointment_id=appointment.id
        )

    if request.method == "POST":

        form = MedicalHistoryForm(request.POST)

        if form.is_valid():

            history = form.save(commit=False)

            history.patient = patient

            history.save()

            return redirect(
                "consultation",
                appointment_id=appointment.id
            )

    else:

        form = MedicalHistoryForm()

    context = {

        "form": form,

        "patient": patient,

        "appointment": appointment,

    }

    return render(
        request,
        "doctor/create_history.html",
        context
    )