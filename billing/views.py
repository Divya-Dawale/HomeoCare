from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from doctors.models import DoctorSettings
from prescriptions.models import Prescription
from .models import Bill
from decimal import Decimal


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

    doctor_settings = DoctorSettings.objects.first()

    if doctor_settings:

        consultation_fee = (
            doctor_settings.consultation_fee
        )

        weekly_medicine_fee = (
            doctor_settings.medicine_fee_7_days
        )

    else:

        consultation_fee = Decimal("500")

        weekly_medicine_fee = Decimal("200")

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

        duration_days = get_duration_days(
            prescription.duration
        )

        medicine_fee = round(
            (weekly_medicine_fee / Decimal("7")) * duration_days
        )

        if duration_days >= 60:

            medicine_fee = medicine_fee * Decimal("0.85")

        elif duration_days >= 30:

            medicine_fee = medicine_fee * Decimal("0.90")


        final_amount = (
            consultation_fee + medicine_fee
        )


        payment_method = request.POST.get(
            "payment_method"
        )


        bill = Bill.objects.create(

            patient=prescription.patient,

            prescription=prescription,

            consultation_fee=consultation_fee,

            medicine_fee=medicine_fee,

            total_amount=final_amount,

            payment_method=payment_method,

            payment_status="paid"

        )


        prescription.billing_done = True
        prescription.save()


        return redirect(
            "receipt",
            bill_id=bill.id
        )

    for prescription in prescriptions:


        if duration_days >= 60:

            medicine_fee = (
                medicine_fee * Decimal("0.85")
            )

        elif duration_days >= 30:

            medicine_fee = (
                medicine_fee * Decimal("0.90")
            )

        prescription.consultation_fee = (
            consultation_fee
        )

        prescription.medicine_fee = (
            medicine_fee
        )

        prescription.total_amount = (
            consultation_fee +
            medicine_fee
        )
    return render(
        request,
        "billing/billing_list.html",
        {
            "prescriptions": prescriptions,
        
        }
    )
    
        


def receipt(
    request,
    bill_id
):

    bill = get_object_or_404(
        Bill,
        id=bill_id
    )

    if request.method == "POST":

        bill.printed = True
        bill.save()

    return render(
        request,
        "billing/receipt.html",
        {
            "bill": bill
        }
    )
    