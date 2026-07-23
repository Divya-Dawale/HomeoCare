from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        'patient_id',
        'full_name',
        'phone',
        'gender',
        'created_at'
    )

    search_fields = (
        'patient_id',
        'full_name',
        'phone'
    )

    list_filter = (
        'gender',
        'created_at'
    )

    ordering = (
        '-created_at',
    )