from django.contrib import admin
from .models import (
    MedicalHistory,
    MedicalRecord,
    DoctorSettings
)

admin.site.register(MedicalRecord)
admin.site.register(MedicalHistory)


@admin.register(DoctorSettings)
class DoctorSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "consultation_fee",
        "medicine_fee_7_days",
        "max_patients_per_day",
        "phone",
        "email",
        "opening_time",
        "closing_time",
    )