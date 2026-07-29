from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.billing_list,
        name="billing"
    ),

    path(
        "receipt/<int:bill_id>/",
        views.receipt,
        name="receipt"
    ),

    
]