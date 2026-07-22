from django.shortcuts import render

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