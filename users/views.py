from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def staff_login(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            if user.groups.filter(
                name="Receptionist"
            ).exists():

                return redirect(
                    "receptionist_dashboard"
                )

            elif user.groups.filter(
                name="Doctor"
            ).exists():

                return redirect(
                    "doctor_dashboard"
                )

        else:

            error = "Invalid username or password."

    return render(
        request,
        "users/login.html",
        {
            "error": error
        }
    )