from django.urls import path
from . import views

urlpatterns = [

    path(
        "history/",
        views.appointment_history,
        name="appointment_history"
    ),

]