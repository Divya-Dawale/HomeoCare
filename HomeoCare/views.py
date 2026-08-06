from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

def book_appointment(request):
    return render(request,'public/appointment.html')
def patient_status(request):
    return render(request, 'public/patient_status.html')
def about(request):
    return render(request,'public/about.html')

def services(request):
    return render(request,'public/services.html')
def home(request):
    return render(request, 'public/home.html')

def test_email(request):

    send_mail(
        "HomeoCare Test Email",
        "Your HomeoCare email system is working successfully.",
        None,
        ["divyadawale2009@gmail.com"],
        fail_silently=False,
    )

    return HttpResponse("Email sent successfully")