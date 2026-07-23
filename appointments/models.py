from django.db import models
from patients.models import Patient


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateField()

    reason_for_visit = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient.full_name} - {self.appointment_date}"
class AppointmentRequest(models.Model):

    REQUEST_TYPE = [
        ('new', 'New Patient'),
        ('existing', 'Existing Patient'),
    ]

    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE
    )

    full_name = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    patient_id = models.CharField(
        max_length=20,
        blank=True
    )

    preferred_date = models.DateField()

    reason_for_visit = models.TextField()

    status = models.CharField(
        max_length=20,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.request_type} - {self.phone}"