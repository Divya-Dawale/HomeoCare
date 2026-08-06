from django.urls import path
from django.contrib.auth import views as auth_views
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

    path(
        "register/",
        views.register,
        name="register"
    ),

    # Forgot Password
    # Forgot Password

path(
    "forgot-password/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/forgot_password.html"
    ),
    name="forgot_password",
),
path(
    "forgot-password/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ),
    name="password_reset_complete",
),
]