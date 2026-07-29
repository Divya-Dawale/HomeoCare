from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from doctors.models import MedicalRecord


class Prescription(models.Model):
    billing_done = models.BooleanField(
    default=False
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE
    )

    medicine_name = models.CharField(
        max_length=200
    )

    dosage = models.CharField(
        max_length=100
    )

    frequency = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    duration = models.CharField(
        max_length=100,
        blank=True
    )

    instructions = models.TextField()

    medicine_given = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.patient.full_name} - "
            f"{self.medicine_name}"
        )