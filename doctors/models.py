from django.db import models
from patients.models import Patient
from appointments.models import Appointment


class MedicalRecord(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    symptoms = models.TextField()

    observations = models.TextField(
        blank=True
    )

    diagnosis_notes = models.TextField()

    follow_up_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.patient.full_name} "
            f"- Record #{self.id}"
        )

class MedicalHistory(models.Model):

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE
    )

    allergies = models.TextField(
        blank=True
    )

    past_diseases = models.TextField(
        blank=True
    )

    family_history = models.TextField(
        blank=True
    )

    blood_pressure = models.CharField(
        max_length=30,
        blank=True
    )

    weight = models.CharField(
        max_length=20,
        blank=True
    )

    current_problem = models.TextField(
        blank=True
    )

    additional_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Medical History - {self.patient.full_name}"


