from django.db import models
from django.conf import settings


class Patient(models.Model):

    patient_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="patient"
    )

    full_name = models.CharField(
        max_length=100 
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=10
    )

    address = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.patient_id:

            last_patient = Patient.objects.order_by('-id').first()

            if last_patient:
                last_id = int(last_patient.patient_id[2:])
                new_id = last_id + 1
            else:
                new_id = 1

            self.patient_id = f"HC{new_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_id} - {self.full_name}"


class MedicalHistory(models.Model):

    patient = models.OneToOneField(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="medical_history"
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True
    )

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    allergies = models.TextField(
        blank=True
    )

    chronic_diseases = models.TextField(
        blank=True
    )

    previous_surgeries = models.TextField(
        blank=True
    )

    family_history = models.TextField(
        blank=True
    )

    current_medications = models.TextField(
        blank=True
    )

    smoking = models.BooleanField(
        default=False
    )

    alcohol = models.BooleanField(
        default=False
    )

    emergency_contact = models.CharField(
        max_length=15,
        blank=True
    )

    emergency_person = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.patient.full_name} History"