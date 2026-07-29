from django.db import models
from patients.models import Patient
from prescriptions.models import Prescription


class Bill(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    medicine_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=20
    )

    payment_status = models.CharField(
        max_length=20,
        default="paid"
    )

    printed = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
         return f"{self.patient.patient_id} - {self.patient.full_name}"
    