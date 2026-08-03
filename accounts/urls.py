from django.urls import path
from . import views

urlpatterns = [

    path(
        "staff/login/",
        views.staff_login,
        name="staff_login"
    ),
    path(
    "logout/",
    views.logout_user,
    name="logout"
    ),
    path("register/", views.register, name="register"),
]