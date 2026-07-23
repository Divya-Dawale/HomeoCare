from django.db import models


class Patient(models.Model):

    patient_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
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