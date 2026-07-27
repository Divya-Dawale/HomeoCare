from django.urls import path
from . import views

urlpatterns = [

    path(
        "staff/login/",
        views.staff_login,
        name="staff_login"
    ),

]