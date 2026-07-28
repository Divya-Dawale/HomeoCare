from django.contrib import admin
from .models import MedicalHistory, MedicalRecord


admin.site.register(MedicalRecord)
admin.site.register(MedicalHistory)
