from django.contrib import admin
from .models import MedicalRecord
from .models import MedicalHistory

admin.site.register(MedicalRecord)
admin.site.register(MedicalHistory)
