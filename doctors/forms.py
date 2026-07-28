from django import forms
from .models import MedicalHistory
from .models import MedicalRecord

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