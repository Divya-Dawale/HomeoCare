from django import forms
from .models import MedicalHistory, MedicalRecord

class MedicalHistoryForm(forms.ModelForm):

    class Meta:

        model = MedicalHistory

        fields = [

            "allergies",

            "past_diseases",

            "family_history",

            "blood_pressure",

            "weight",

            "current_problem",

            "additional_notes",

        ]

        widgets = {

            "allergies": forms.Textarea(attrs={"rows":2}),

            "past_diseases": forms.Textarea(attrs={"rows":2}),

            "family_history": forms.Textarea(attrs={"rows":2}),

            "current_problem": forms.Textarea(attrs={"rows":3}),

            "additional_notes": forms.Textarea(attrs={"rows":3}),

        }

class MedicalRecordForm(forms.ModelForm):

    class Meta:

        model = MedicalRecord

        fields = [

            "symptoms",

            "observations",

            "diagnosis_notes",

            "follow_up_notes",

        ]

        widgets = {

            "symptoms": forms.Textarea(attrs={"rows":4}),

            "observations": forms.Textarea(attrs={"rows":4}),

            "diagnosis_notes": forms.Textarea(attrs={"rows":4}),

            "follow_up_notes": forms.Textarea(attrs={"rows":4}),

        }
from django import forms
from .models import DoctorSettings

class DoctorSettingsForm(forms.ModelForm):

    class Meta:

        model = DoctorSettings

        fields = [
            "consultation_fee",
            "medicine_fee_7_days",
            "max_patients_per_day",
        ]
from accounts.models import User

class DoctorProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "email"
        ]