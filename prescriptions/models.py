from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from doctors.models import MedicalRecord


class Prescription(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='prescriptions'
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

    instructions = models.TextField()

    duration = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient.full_name} - {self.medicine_name}"