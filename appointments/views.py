from django.shortcuts import render
from datetime import datetime
from .models import Appointment
from django.db.models import Q

def appointment_history(request):

    appointments = Appointment.objects.filter(
        status="completed"
    )

    search = request.GET.get("search")

    if search:

        appointments = appointments.filter(

            Q(patient__full_name__icontains=search) |

            Q(patient__patient_id__icontains=search)

        )

    appointments = appointments.order_by(
        "-appointment_date"
    )

    return render(
        request,
        "appointments/history.html",
        {
            "appointments": appointments
        }
    )