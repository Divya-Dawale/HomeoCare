from django.urls import path
from . import views

urlpatterns = [

    path(
        'dashboard/',
        views.doctor_dashboard,
        name='doctor_dashboard'
    ),

    path(
        'patient-queue/',
        views.patient_queue,
        name='patient_queue'
    ),

    path(
        'medical-records/',
        views.medical_records,
        name='medical_records'
    ),

    path(
        'prescriptions/',
        views.prescriptions,
        name='prescriptions'
    ),

    path(
    "consultation/<int:appointment_id>/",
    views.consultation,
    name="consultation",
    ),
    path(
    "history/create/<int:appointment_id>/",
    views.create_medical_history,
    name="create_medical_history",
    ),
    path(
    "create-history/<int:appointment_id>/",
    views.create_medical_history,
    name="create_medical_history"
    ),
    path(
    'revenue/',
    views.doctor_revenue,
    name='doctor_revenue'
    ),
    path(
    "settings/",
    views.doctor_settings,
    name="doctor_settings"
    ),

   path(
    'profile/',
    views.doctor_profile,
    name='doctor_profile'
    ),

path(
    "settings/change-password/",
    views.doctor_change_password,
    name="doctor_change_password"
),
path(
    "clinic-management/",
    views.clinic_management,
    name="clinic_management"
),
]