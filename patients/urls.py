from django.urls import path
from . import views

urlpatterns = [
     path(
        "dashboard/",
        views.patient_dashboard,
        name="patient_dashboard"
    ),

    path(
    "appointments/",
    views.patient_appointments,
    name="patient_appointments",
),
path(
    "appointments/cancel/<int:appointment_id>/",
    views.cancel_appointment,
    name="cancel_appointment"
),
    path(
    "medical-records/",
    views.medical_records,
    name="patient_records"
),
path(
    "prescriptions/",
    views.patient_prescriptions,
    name="patient_prescriptions"
),
path(
    "bills/",
    views.patient_bills,
    name="patient_bills"
),

path(
    "settings/",
    views.patient_settings,
    name="patient_settings"
),
path(
    "change-password/",
    views.patient_change_password,
    name="patient_change_password",
),
path(
    "profile/",
    views.patient_profile,
    name="patient_profile",
),
path(
    "history/",
    views.patient_history,
    name="patient_history",
),
path(
    "chatbot/appointment/",
    views.patient_chatbot_appointment,
    name="patient_chatbot_appointment"
),

path(
    "chatbot/medical-records/",
    views.patient_chatbot_medical_records,
    name="patient_chatbot_medical_records"
),

path(
    "chatbot/prescriptions/",
    views.patient_chatbot_prescriptions,
    name="patient_chatbot_prescriptions"
),

path(
    "chatbot/bills/",
    views.patient_chatbot_bills,
    name="patient_chatbot_bills"
),

path(
    "chatbot/history/",
    views.patient_chatbot_history,
    name="patient_chatbot_history"
),
]
