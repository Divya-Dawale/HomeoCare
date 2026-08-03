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

    height = models.PositiveIntegerField(
    null=True,
    blank=True
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True
    )

    physical_build = models.CharField(
        max_length=50,
        blank=True
    )

    side_affinity = models.CharField(
        max_length=30,
        blank=True
    )

    thermal_state = models.CharField(
        max_length=30,
        blank=True
    )

    location_extension = models.TextField(
    blank=True
    )

    aggravation_factors = models.JSONField(
        default=list,
        blank=True
    )

    amelioration_factors = models.JSONField(
        default=list,
        blank=True
    )

    concomitants = models.TextField(
        blank=True
    )

    etiology = models.CharField(
        max_length=100,
        blank=True
    )

    etiology_notes = models.TextField(
        blank=True
    )

    diet_type = models.CharField(
    max_length=30,
    blank=True
    )

    meal_pattern = models.CharField(
        max_length=50,
        blank=True
    )

    appetite_scale = models.CharField(
        max_length=50,
        blank=True
    )

    thirst_pattern = models.CharField(
        max_length=100,
        blank=True
    )

    food_cravings = models.JSONField(
        default=list,
        blank=True
    )

    food_aversions = models.JSONField(
        default=list,
        blank=True
    )

    food_intolerances = models.JSONField(
        default=list,
        blank=True
    )

    sleep_posture = models.CharField(
        max_length=50,
        blank=True
    )
    social_disposition = models.CharField(
    max_length=50,
    blank=True
    )

    temperament = models.JSONField(
        default=list,
        blank=True
    )

    pace_of_actions = models.CharField(
        max_length=50,
        blank=True
    )

    orderliness = models.CharField(
        max_length=50,
        blank=True
    )

    self_perception = models.CharField(
        max_length=100,
        blank=True
    )

    criticism_response = models.CharField(
        max_length=100,
        blank=True
    )

    ambition = models.CharField(
        max_length=100,
        blank=True
        )

    future_outlook = models.CharField(
        max_length=100,
        blank=True
    )

    anger_reaction = models.CharField(
        max_length=100,
        blank=True
    )

    consolation_reaction = models.CharField(
        max_length=100,
        blank=True
    )

    weeping_tendency = models.CharField(
        max_length=100,
        blank=True
    )

    memory_concentration = models.JSONField(
        default=list,
        blank=True
    )

    fears = models.JSONField(
        default=list,
        blank=True
    )

    dream_themes = models.JSONField(
        default=list,
        blank=True
    )
    suppression_history = models.JSONField(
    default=list,
    blank=True
    )

    vaccination_effects = models.CharField(
        max_length=100,
        blank=True
    )

    vaccination_notes = models.TextField(
        blank=True
    )

    family_miasms = models.JSONField(
        default=list,
        blank=True
    )
    def __str__(self):

        return f"Medical History - {self.patient.full_name}"


from django.db import models
from accounts.models import User

class DoctorSettings(models.Model):

    doctor = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=500
    )

    medicine_fee_7_days = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=200
    )

    max_patients_per_day = models.PositiveIntegerField(
        default=20
    )

    phone = models.CharField(
    max_length=10,
    blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    opening_time = models.TimeField(
        null=True,
        blank=True
    )

    closing_time = models.TimeField(
        null=True,
        blank=True
    )

    google_map_link = models.TextField(
    blank=True
)

    dark_mode = models.BooleanField(
        default=False
    )