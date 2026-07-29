from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from prescriptions.models import Prescription
from .models import Bill


CONSULTATION_FEE = 100
WEEKLY_MEDICINE_FEE = 150


def get_duration_days(duration):

    duration = duration.lower()

    if "60" in duration:
        return 60

    elif "30" in duration or "month" in duration:
        return 30

    elif "15" in duration:
        return 15

    elif "7" in duration:
        return 7

    return 7


def billing_list(request):

    prescriptions = Prescription.objects.filter(
        status="given",
        billing_done=False
    ).order_by("-created_at")

    if request.method == "POST":

        prescription_id = request.POST.get(
            "prescription_id"
        )

        prescription = get_object_or_404(
            Prescription,
            id=prescription_id
        )

        final_amount = request.POST.get(
            "final_amount"
        )

        payment_method = request.POST.get(
            "payment_method"
        )

        duration_days = get_duration_days(
            prescription.duration
        )

        daily_rate = WEEKLY_MEDICINE_FEE / 7

        medicine_fee = round(
            daily_rate * duration_days,
            -1
        )

        if duration_days >= 60:

            medicine_fee = round(
                medicine_fee * 0.85,
                -1
            )

        elif duration_days >= 30:

            medicine_fee = round(
                medicine_fee * 0.90,
                -1
            )

        Bill.objects.create(

            patient=prescription.patient,

            prescription=prescription,

            consultation_fee=CONSULTATION_FEE,

            medicine_fee=medicine_fee,

            total_amount=final_amount,

            payment_method=payment_method,

            payment_status="paid"

        )
        prescription.billing_done = True
        prescription.save()

        return redirect(
            "billing"
        )

    for prescription in prescriptions:

        duration_days = get_duration_days(
            prescription.duration
        )

        daily_rate = WEEKLY_MEDICINE_FEE / 7

        medicine_fee = round(
            daily_rate * duration_days,
            -1
        )

        if duration_days >= 60:

            medicine_fee = round(
                medicine_fee * 0.85,
                -1
            )

        elif duration_days >= 30:

            medicine_fee = round(
                medicine_fee * 0.90,
                -1
            )

        prescription.consultation_fee = (
            CONSULTATION_FEE
        )

        prescription.medicine_fee = (
            medicine_fee
        )

        prescription.total_amount = (
            CONSULTATION_FEE
            + medicine_fee
        )

    return render(
        request,
        "billing/billing_list.html",
        {
            "prescriptions": prescriptions
        }
    )