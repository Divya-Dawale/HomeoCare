from django.urls import path
from . import views

urlpatterns = [

    path(
        'dashboard/',
        views.dashboard,
        name='receptionist_dashboard'
    ),

    path(
        'requests/',
        views.appointment_requests,
        name='appointment_requests'
    ),

    path(
        'patients/',
        views.patients,
        name='patients'
    ),

    path(
        'appointments/',
        views.appointments,
        name='appointments'
    ),
    path(
    "appointment-requests/<int:request_id>/",
    views.request_detail,
    name="request_detail",
    ),
    path(
    "approve-request/<int:request_id>/",
    views.approve_request,
    name="approve_request",
    ),
    path(
    "reject-request/<int:request_id>/",
    views.reject_request,
    name="reject_request",
    ),
    path(
    "patients/<int:patient_id>/",
    views.patient_detail,
    name="patient_detail",
    ),

]